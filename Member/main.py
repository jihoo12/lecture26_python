import member_manager as m
import sys
service = m.MemberService()

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