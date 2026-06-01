from Member.member import Member
#====================
# 회원 데이터 접근 (CRUD) : MemberDAO
class MemberDAO:
    def __init__(self):
        self.__memberDB = {}
    
    def insert_member(self, member):
        if self.is_exist(member.get_id()):
            return False
        self.__memberDB[member.get_id()] = member
        return True

    def is_exist(self, id):
        if id in self.__memberDB.keys() : return True
        return False
    
    def get_member_info(self, id):
        if self.is_exist(id):
            return self.__memberDB[id]
        else:
            return None
        
    def get_all_members(self):
        if self.__memberDB:
            return list(self.__memberDB.values())
    
    def update_member_info(self, id, member):
        if self.is_exist(id):
            self.__memberDB[id] = member
            return True
        return False

    def remove_member(self, id):
        if self.is_exist(id):
            self.__memberDB.pop(id)
            return True
        return False
    
# 클래스 동작 테스트 (단위테스트, unit test)
if __name__ == '__main__':
    dao = MemberDAO()
    print(dao.is_exist('hyejeong'))

    member = Member('hyejeong', '1234', '이혜정')
    dao.insert_member(member)
    member = Member('curi', '1234', '1234')
    dao.insert_member(member)
    print(dao.get_member_info('hyejeong'))
    print(dao.get_member_info('curi'))

    members = dao.get_all_members()
    for member in members:
        print(member)

    member = dao.get_member_info('hyejeong')
    if member:
        member.set_password('1111')
        dao.update_member_info('hyejeong', member)
    
    members = dao.get_all_members()
    for member in members:
        print(member)

    dao.remove_member('hyejeong')
    members = dao.get_all_members()
    for member in members:
        print(member)