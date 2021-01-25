from webull import paper_webull

# A helper class for managing the Webull account object.


class WebullHelper:
    wb = paper_webull()
    mfa = None

    # Attempts to login using the username, password and multi-factor authentication is needed.
    # Previously used MFA is required to login. If no MFA is stored, MFA will be requested.

    def login(self, username, password, mfa):

        if mfa != '':
            self.__store_mfa(mfa)

        self.mfa = self.__retrieve_mfa()
        if self.mfa is not None:
            try:
                self.wb.login(username, password, mfa=self.mfa)
                self.wb.get_account_id()
                return True
            except:
                print('Invalid login credentials. Try again. MFA not none')
                return False
        else:
            try:
                self.wb.login(username, password, mfa)
                self.wb.get_account_id()
                self.__store_mfa(mfa)
                return True
            except:
                print('Invalid login credentials. Try again.')

    def logout(self):
        self.wb.logout()

    def get_webull_object(self):
        return self.wb

    def get_new_mfa(self, username):
        return self.wb.get_mfa(username)

    def __store_mfa(self, mfa):
        with open("mfa.txt", "w") as f:  # in write mode
            f.write("{}".format(mfa))

    def __retrieve_mfa(self):
        try:
            with open("mfa.txt") as f:  # in read mode, not in write mode, careful
                rd = f.readline()
            return int(rd)
        except:
            print('no mfa file found.')
            return None
