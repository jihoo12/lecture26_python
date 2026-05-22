#======================
# 데이터 모델 정의 : Member
class Member:
    def __init__(self, id, password, name):
        self.__member_no = 0
        self.__id = id
        self.__password = password
        self.__name = name

    def get_member_no(self):
        return self.__member_no
    def get_id(self):
        return self.__id
    def get_password(self):
        return self.__password
    def get_name(self):
        return self.__name
    def set_password(self, password):
        self.__password = password
    
    def __str__(self):
        return f'{self.__member_no}\t{self.__id}\t{self.__name}\t{self.__password}'   

#==================
# 회원 관리 서비스 로직 (Controller) : MemberService
class MemberService:
    def __init__(self, memberDao):
        self.__dao = memberDao

    def join(self, member):
        # 이미 있는 아이디인지 확인
        if self.__dao.is_exist(member.get_id()):
            return False
        self.__dao.insert_member(member)
        return True

    def login(self, id, password):
        member = self.__dao.get_member_info(id)
        if member:
            if password == member.get_password():
                return id
        return None
    
    def list_members(self):
        member_list = self.__dao.get_all_members()
        return member_list

#====================
# 회원 데이터 접근 (CRUD) : MemberDAO
class MemberDAO:
    def __init__(self):
        self.__memberDB = {}
    
    def insert_member(self, member):
        self.__memberDB[member.get_id()] = member

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
    