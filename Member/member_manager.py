import sys

# 1. 회원 정보 클래스
class Member:
    def __init__(self, mem_no, mem_id, pw, name, phone, address):
        self.mem_no = mem_no
        self.mem_id = mem_id
        self.pw = pw
        self.name = name
        self.phone = phone
        self.address = address
        self.balance = 0  # 예치금 잔액 속성 (초기값 0원)

    def __str__(self):
        return f"[{self.mem_no}] ID: {self.mem_id} | 이름: {self.name} | 연락처: {self.phone} | 잔액: {self.balance:,}원"


# 2. 회원 관리 로직 클래스
class MemberService:
    def __init__(self):
        self.members = []       # Member 객체들을 담을 리스트
        self.count = 0          # 회원 번호 자동 생성을 위한 카운터
        self.current_user = None  # 현재 로그인한 회원을 저장 (None이면 로그아웃 상태)

    # [신규] 로그인 기능
    def login(self):
        print("\n--- [로 그 인] ---")
        if self.current_user:
            print(f"이미 {self.current_user.name}님으로 로그인되어 있습니다.")
            return

        mem_id = input("아이디: ")
        pw = input("비밀번호: ")

        # 아이디와 비밀번호가 동시에 일치하는 회원 찾기
        for m in self.members:
            if m.mem_id == mem_id and m.pw == pw:
                self.current_user = m
                print(f"\n환영합니다, {m.name}님! 로그인이 완료되었습니다.")
                return
        
        print("아이디 또는 비밀번호가 일치하지 않습니다.")

    # [신규] 로그아웃 기능
    def logout(self):
        print("\n--- [로 그 아 웃] ---")
        if not self.current_user:
            print("로그인 상태가 아닙니다.")
            return
        
        print(f"{self.current_user.name}님이 로그아웃 되었습니다.")
        self.current_user = None

    # 회원 가입
    def register(self):
        print("\n--- [회원 가입] ---")
        mem_id = input("아이디: ")
        
        # 중복 아이디 체크 추가
        for m in self.members:
            if m.mem_id == mem_id:
                print("이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.")
                return

        pw = input("비밀번호: ")
        name = input("이름: ")
        phone = input("전화번호: ")
        address = input("주소: ")
        
        self.count += 1
        new_member = Member(self.count, mem_id, pw, name, phone, address)
        self.members.append(new_member)
        print(f"회원가입이 완료되었습니다. (회원번호: {self.count})")

    # 회원 목록 출력 (관리자 기능 혹은 전체 확인용)
    def show_list(self):
        print("\n--- [회원 목록] ---")
        if not self.members:
            print("등록된 회원이 없습니다.")
            return
        for m in self.members:
            print(m)

    # 회원 상세 정보 (내 정보 보기)
    def show_detail(self):
        print("\n--- [내 정보 상세조회] ---")
        # 로그인 체크
        if not self.current_user:
            print("로그인이 필요한 서비스입니다.")
            return

        member = self.current_user
        print(f"번호: {member.mem_no}")
        print(f"ID: {member.mem_id}")
        print(f"이름: {member.name}")
        print(f"전화번호: {member.phone}")
        print(f"주소: {member.address}")
        print(f"잔액: {member.balance:,}원")

    # 회원 정보 수정
    def update_member(self):
        print("\n--- [내 정보 수정] ---")
        # 로그인 체크
        if not self.current_user:
            print("로그인이 필요한 서비스입니다.")
            return

        member = self.current_user
        print(f"{member.name}님의 정보를 수정합니다. (엔터 입력 시 기존 정보 유지)")
        new_phone = input(f"변경할 전화번호[{member.phone}]: ")
        new_addr = input(f"변경할 주소[{member.address}]: ")
        
        if new_phone: member.phone = new_phone
        if new_addr: member.address = new_addr
        print("정보 수정이 완료되었습니다.")

    # 회원 탈퇴
    def delete_member(self):
        print("\n--- [회원 탈퇴] ---")
        # 로그인 체크
        if not self.current_user:
            print("로그인이 필요한 서비스입니다.")
            return

        member = self.current_user
        confirm = input(f"정말로 탈퇴하시겠습니까? ({member.name}님의 정보와 잔액이 모두 삭제됩니다.) (y/n): ")
        if confirm.lower() == 'y':
            self.members.remove(member)
            self.current_user = None  # 탈퇴 후 로그아웃 처리
            print("탈퇴 처리가 완료되었습니다. 이용해 주셔서 감사합니다.")
        else:
            print("탈퇴를 취소했습니다.")

    # 입금 기능 (돈 넣기)
    def deposit(self):
        print("\n--- [예치금 입금] ---")
        # 로그인 체크
        if not self.current_user:
            print("로그인이 필요한 서비스입니다.")
            return

        member = self.current_user
        try:
            amount = int(input("입금할 금액을 입력하세요: "))
            if amount <= 0:
                print("1원 이상의 금액만 입금할 수 있습니다.")
                return
            member.balance += amount
            print(f"입금이 완료되었습니다. ({member.name}님 현재 잔액: {member.balance:,}원)")
        except ValueError:
            print("금액은 숫자만 입력해주세요.")

    # 출금 기능 (돈 빼기)
    def withdraw(self):
        print("\n--- [예치금 출금] ---")
        # 로그인 체크
        if not self.current_user:
            print("로그인이 필요한 서비스입니다.")
            return

        member = self.current_user
        try:
            amount = int(input("출금할 금액을 입력하세요: "))
            if amount <= 0:
                print("1원 이상의 금액만 출금할 수 있습니다.")
                return
            
            # 잔액 검증
            if member.balance < amount:
                print(f"잔액이 부족합니다. (현재 잔액: {member.balance:,}원)")
            else:
                member.balance -= amount
                print(f"출금이 완료되었습니다. ({member.name}님 현재 잔액: {member.balance:,}원)")
        except ValueError:
            print("금액은 숫자만 입력해주세요.")


# 3. 메인 UI 및 제어
def main():
    service = MemberService()
    
    while True:
        print("\n===== 회원 관리 프로그램 =====")
        # 상단에 로그인 상태 표시 고정
        if service.current_user:
            print(f"[ 로그인 상태: {service.current_user.name}님 ({service.current_user.mem_id}) ]")
        else:
            print("[ 로그인 상태: 로그아웃 ]")
        print("----------------------------")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 로그아웃")
        print("4. 내 정보 보기 (상세정보)")
        print("5. 내 정보 수정")
        print("6. 입금하기")
        print("7. 출금하기")
        print("8. 회원탈퇴")
        print("9. 전체 회원목록 출력 (관리용)")
        print("0. 프로그램 종료")
        print("============================")
        
        try:
            choice = int(input("메뉴 선택: "))
        except ValueError:
            print("숫자만 입력 가능합니다. 다시 선택해주세요.")
            continue
        
        match choice:
            case 1:
                service.register()
            case 2:
                service.login()
            case 3:
                service.logout()
            case 4:
                service.show_detail()
            case 5:
                service.update_member()
            case 6:
                service.deposit()
            case 7:
                service.withdraw()
            case 8:
                service.delete_member()
            case 9:
                service.show_list()
            case 0:
                print("프로그램을 종료합니다.")
                sys.exit()
            case _:
                print("잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()