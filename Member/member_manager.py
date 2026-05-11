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

    def __str__(self):
        return f"[{self.mem_no}] ID: {self.mem_id} | 이름: {self.name} | 연락처: {self.phone}"


# 2. 회원 관리 로직 클래스
class MemberService:
    def __init__(self):
        self.members = []  # Member 객체들을 담을 리스트
        self.count = 0     # 회원 번호 자동 생성을 위한 카운터

    # 회원 가입
    def register(self):
        print("\n--- [회원 가입] ---")
        mem_id = input("아이디: ")
        pw = input("비밀번호: ")
        name = input("이름: ")
        phone = input("전화번호: ")
        address = input("주소: ")
        
        self.count += 1
        new_member = Member(self.count, mem_id, pw, name, phone, address)
        self.members.append(new_member)
        print(f"회원가입이 완료되었습니다. (회원번호: {self.count})")

    # 회원 목록 출력
    def show_list(self):
        print("\n--- [회원 목록] ---")
        if not self.members:
            print("등록된 회원이 없습니다.")
            return
        for m in self.members:
            print(m)

    # 회원 상세 정보
    def show_detail(self):
        print("\n--- [회원 상세 정보] ---")
        mem_no = int(input("조회할 회원번호를 입력하세요: "))
        member = self.find_member(mem_no)
        if member:
            print(f"번호: {member.mem_no}")
            print(f"ID: {member.mem_id}")
            print(f"이름: {member.name}")
            print(f"전화번호: {member.phone}")
            print(f"주소: {member.address}")
        else:
            print("해당 번호의 회원을 찾을 수 없습니다.")

    # 회원 정보 수정
    def update_member(self):
        print("\n--- [회원 정보 수정] ---")
        mem_no = int(input("수정할 회원번호를 입력하세요: "))
        member = self.find_member(mem_no)
        if member:
            print(f"{member.name}님의 정보를 수정합니다. (엔터 입력 시 기존 정보 유지)")
            new_phone = input(f"변경할 전화번호[{member.phone}]: ")
            new_addr = input(f"변경할 주소[{member.address}]: ")
            
            if new_phone: member.phone = new_phone
            if new_addr: member.address = new_addr
            print("정보 수정이 완료되었습니다.")
        else:
            print("해당 번호의 회원을 찾을 수 없습니다.")

    # 회원 탈퇴
    def delete_member(self):
        print("\n--- [회원 탈퇴] ---")
        mem_no = int(input("탈퇴할 회원번호를 입력하세요: "))
        member = self.find_member(mem_no)
        if member:
            self.members.remove(member)
            print(f"회원번호 {mem_no}번 회원이 탈퇴 처리되었습니다.")
        else:
            print("해당 번호의 회원을 찾을 수 없습니다.")

    # 공통: 회원 번호로 객체 찾기 보조 함수
    def find_member(self, mem_no):
        for m in self.members:
            if m.mem_no == mem_no:
                return m
        return None


# 3. 메인 UI 및 제어
def main():
    service = MemberService()
    
    while True:
        print("\n===== 회원 관리 프로그램 =====")
        print("1. 회원가입")
        print("2. 회원목록")
        print("3. 상세정보")
        print("4. 정보수정")
        print("5. 회원탈퇴")
        print("0. 프로그램 종료")
        print("============================")
        
        choice = input("메뉴 선택: ")
        
        if choice == '1':
            service.register()
        elif choice == '2':
            service.show_list()
        elif choice == '3':
            service.show_detail()
        elif choice == '4':
            service.update_member()
        elif choice == '5':
            service.delete_member()
        elif choice == '0':
            print("프로그램을 종료합니다.")
            sys.exit()
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()