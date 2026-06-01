from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    start_menu = ['종료', '로그인', '회원가입']
    banking_menu = []
    member_myinfo_menu = []
    admin_menu = []
    admin_account_menu = []
    admin_member_menu = []

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDAO())

    def main(self):
        self.show_welcome()
        while True:
            menu = self.select_menu(ConsoleBank.select_menu)
            if menu == 0: break
            elif menu == 1:
                pass
            elif menu == 2:
                pass
        self.say_goodbye()

    def show_welcome(self):
        print('======== Hyejeong Console Bank ==========')

    def say_goodbye(self):
        print('>> Hyejeong Console Bank를 이용해 주셔서 감사합니다.')

    def select_menu(self, menu_list):
        return 0

if __name__ == '__main__':
    app = ConsoleBank()
    app.main()