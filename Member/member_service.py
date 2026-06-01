from member_dao import MemberDAO
from member import Member

#==================
# 회원 관리 서비스 로직 (Controller) : MemberService
class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self, memberDao):
        self.__dao = memberDao
        self.join(Member(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD, '관리자'))
        self.current_user = None

    def join(self, member):

        # 대소문자 구별하지 않음
        #member.set_id(member.get_id().lower())
        # if not self.is_valid_id(member.get_id()):
        #     return False
        
        # 이미 있는 아이디인지 확인
        if self.__dao.is_exist(member.get_id()):
            return False
        
        self.__dao.insert_member(member)
        return True

    def login(self, id, password):
        member = self.__dao.get_member_info(id)
        if member:
            if password == member.get_password():
                self.current_user = id
                return True
        return False
    
    def list_members(self):
        return self.__dao.get_all_members()
    
    def logout(self):
        self.current_user = None

    def view_member_info(self, id):
        return self.__dao.get_member_info(id)

    def update_member_info(self, id, member):
        return self.__dao.update_member_info(id, member)
    
    def update_member_password(self, id, org_password, new_password):
        if self.current_user != id: return False
        member = self.__dao.get_member_info(id)
        if not member: return False
        if member.get_password() == org_password:
            member.set_password(new_password)
            return True
        return False
    
    def remove_member(self, id):
        print(self.current_user)
        if self.current_user == id or self.current_user == MemberService.ADMIN_ID:
            return self.__dao.remove_member(id)
        return False

if __name__ == '__main__':
    ms = MemberService(MemberDAO())
    ms.join(Member('hyejeong', '1234', '이혜정'))
    ms.join(Member('curi', '1111', '큐리'))
    members = ms.list_members()
    for member in members:
        print(member)
    ms.login('curi', '1111')
    print(ms.current_user)
    ms.logout()
    print(ms.current_user)
    print(ms.view_member_info('curi'))
    ms.login(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD)
    print(ms.update_member_password('hyejeong', '1234', '4321'))
    print(ms.view_member_info('hyejeong'))
    print(ms.remove_member('hyejeong'))
    print(ms.view_member_info('hyejeong'))