import torch
import torch.nn as nn
import numpy as np
import math
import os

# --- 1. 모델 클래스 정의 ---
class TransformerGenerator(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, nhid, nlayers, dropout=0.2):
        super(TransformerGenerator, self).__init__()
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead, nhid, dropout, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, nlayers)
        self.decoder = nn.Linear(d_model, vocab_size)

    def forward(self, src, src_mask):
        src = self.embedding(src) * math.sqrt(self.d_model)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, src_mask)
        return self.decoder(output)

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)

def generate_square_subsequent_mask(sz, device):
    mask = (torch.triu(torch.ones(sz, sz, device=device)) == 1).transpose(0, 1)
    mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
    return mask

# --- 2. 설정 및 유틸리티 함수 ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
FILE_NAME = 'model.pth'
DATA_PATH = 'data.txt' # 학습할 파일명

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    chars = sorted(list(set(text)))
    char_to_int = {ch: i for i, ch in enumerate(chars)}
    int_to_char = {i: ch for i, ch in enumerate(chars)}
    data = torch.tensor([char_to_int[ch] for ch in text], dtype=torch.long)
    return data, char_to_int, int_to_char, len(chars)

def get_batch(data, seq_length, batch_size):
    ix = torch.randint(len(data) - seq_length, (batch_size,))
    x = torch.stack([data[i:i+seq_length] for i in ix])
    y = torch.stack([data[i+1:i+seq_length+1] for i in ix])
    return x.to(device), y.to(device)

def generate_text(model, start_str, char_to_int, int_to_char, seq_length, length=100, temperature=0.8):
    model.eval()
    input_indices = [char_to_int[ch] for ch in start_str]
    generated = input_indices[:]
    with torch.no_grad():
        for _ in range(length):
            curr_input = torch.tensor([generated[-seq_length:]]).to(device)
            mask = generate_square_subsequent_mask(curr_input.size(1), device)
            output = model(curr_input, mask)
            logits = output[0, -1] / temperature
            probs = torch.softmax(logits, dim=-1)
            next_char_idx = torch.multinomial(probs, num_samples=1).item()
            generated.append(next_char_idx)
    return ''.join([int_to_char[i] for i in generated])

# --- 3. 실행 로직 ---

# 데이터 먼저 로드
if not os.path.exists(DATA_PATH):
    print(f"오류: {DATA_PATH} 파일이 없습니다.")
else:
    data, char_to_int, int_to_char, vocab_size = load_data(DATA_PATH)

    # 하이퍼파라미터
    d_model = 256
    nhead = 8
    nhid = 512
    nlayers = 6
    seq_length = 100
    batch_size = 64

    # 모델 생성
    model = TransformerGenerator(vocab_size, d_model, nhead, nhid, nlayers).to(device)

    # 만약 기존에 저장된 모델이 있다면 로드, 없으면 새로 학습
    if os.path.exists(FILE_NAME):
        print("기존 모델 파일을 불러옵니다...")
        checkpoint = torch.load(FILE_NAME, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        # 저장된 딕셔너리 정보 업데이트
        char_to_int = checkpoint['char_to_int']
        int_to_char = checkpoint['int_to_char']
    else:
        print("새로운 학습을 시작합니다...")
        optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)
        criterion = nn.CrossEntropyLoss()
        
        model.train()
        for epoch in range(10000): # 넉넉히 5000번 학습
            src, targets = get_batch(data, seq_length, batch_size)
            mask = generate_square_subsequent_mask(seq_length, device)
            output = model(src, mask)
            loss = criterion(output.view(-1, vocab_size), targets.view(-1))
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if epoch % 100 == 0:
                print(f'Epoch {epoch}, Loss: {loss.item():.4f}')

        # 학습 종료 후 저장
        torch.save({
            'model_state_dict': model.state_dict(),
            'char_to_int': char_to_int,
            'int_to_char': int_to_char,
            'vocab_size': vocab_size,
            'd_model': d_model, 'nhead': nhead, 'nhid': nhid, 'nlayers': nlayers, 'seq_length': seq_length
        }, FILE_NAME)
        print("학습 완료 및 모델 저장 성공!")

    # --- 최종 문장 생성 ---
    print("\n--- 생성 결과 ---")
    print(generate_text(model, "joy", char_to_int, int_to_char, seq_length, length=5000))