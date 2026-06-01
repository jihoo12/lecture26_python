from account import Account

class AccountDAO:
    def __init__(self):
        self.__accountDB = {} # 계좌번호 : account 객체
    
    def insert_account(self, account):
        account_no = account.get_account_no()
        if account_no not in self.__accountDB:
            self.__accountDB[account_no] = account
            return True
        return False

    def select_account_by_account_no(self, account_no):
        if account_no in self.__accountDB:
            return self.__accountDB[account_no]
        return None

    def select_accounts_by_member_id(self, member_id):
        account_list = []
        for account in self.__accountDB.values():
            if account.get_owner() == member_id:
                account_list.append(account)
            
        if len(account_list): return account_list
        return None

    def select_all_accounts(self):
        account_list = list(self.__accountDB.values())
        if len(account_list):
            return account_list
        return None

    def update_account(self, account_no, account):
        if account_no in self.__accountDB:
            self.__accountDB[account_no] = account
            return True
        return False

    def delete_account(self, account_no):
        if account_no in self.__accountDB:
            self.__accountDB.pop(account_no)
            return True
        return False

if __name__ == '__main__':
    dao = AccountDAO()
    ac_list = dao.select_all_accounts()
    print(ac_list)
    dao.insert_account(Account('111111', 'hyejeong', 10000, '1234'))
    dao.insert_account(Account('111112', 'curi', 20000, '1234'))
    dao.insert_account(Account('111113', 'curi', 200000, '1234'))
    for account in dao.select_all_accounts():
        print(account)
    print(dao.select_account_by_account_no('111114'))
    for account in dao.select_accounts_by_member_id('hyejeong'):
        print(account)
    print()
    print(dao.select_account_by_account_no('111112'))
    dao.update_account('111112', Account('111112', 'curi', 300000, '1234'))
    print(dao.select_account_by_account_no('111112'))
    print()
    dao.delete_account('111113')
    print(dao.select_account_by_account_no('111113'))