from kivy.uix.screenmanager import Screen,ScreenManager
from navdrawer import ContentNavigationDrawer
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
import globalvariables
import connection
import ibm_db

class SettingsWindow(Screen):
    def load_settings_page(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)

class ApprovalsWindow(Screen):
    conlist = [] # list of contacts selected for aproval or rejection
    def load_approval_page(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        query = f'''SELECT MEMORG.NAME AS ONAME, NEWCON.FIRST_NAME||' '||NEWCON.LAST_NAME AS NAME, 
        NEWCON.EMAIL AS EMAIL
        FROM CONTACT NEWCON, CONTACT_ORG CONORG, 
        CONTACT_ORG MEMCON, ORG MEMORG
        WHERE NEWCON.CONTACT_ID = CONORG.CONTACT_ID
        AND CONORG.STATUS='N' AND CONORG.MEMBER_FLAG='P'
        AND MEMORG.ORG_ID = CONORG.ORG_ID
        AND CONORG.ORG_ID = MEMCON.ORG_ID
        AND MEMCON.CONTACT_ID={globalvariables.var_userid}
        AND MEMCON.STATUS='Y'
        AND MEMCON.MEMBER_FLAG='Y' '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        txnlist = ibm_db.fetch_both(stmt)
        if txnlist is False :
            warn_label = MDLabel(pos_hint = {'center_x':0.5, 'center_y':0.5},font_size = '10sp',
            text = "You do not have any approvals")
            self.ids['approval_float_lay'].add_widget(warn_label)
        else:
            print(txnlist)
            alist=[]
            while(txnlist):
                alist.append([str(txnlist[0]),txnlist[1],txnlist[2]])
                txnlist = ibm_db.fetch_both(stmt)
            data_tables = MDDataTable(
                size_hint=(1, 1),
                rows_num=100,
                check=True,
                pos_hint = {'center_x':0.5, 'center_y':0.5},
                column_data=[
                    ("Group", dp(40)),
                    ("Name", dp(40)),
                    ("Email", dp(40)),
                ],
                row_data=[(f"{i[0]}",f"{i[1]}",f"{i[2]}") for i in alist]
                )
            data_tables.bind(on_check_press=self.on_check_press)
            self.ids['approval_float_lay'].add_widget(data_tables)
            #Approve Button
            approve_button = MDFillRoundFlatIconButton(text="APPROVE",
            pos_hint={'center_x':0.3, 'center_y':0.2}, icon="thumb-up-outline", on_release=lambda x: self.approvereq())
            approve_button.md_bg_color= 0.211, 0.678, 0.054, 1 #Green color
            self.ids['approval_float_lay'].add_widget(approve_button)
            #Reject Button
            reject_button = MDFillRoundFlatIconButton(text="REJECT",
            pos_hint={'center_x':0.7, 'center_y':0.2}, icon="thumb-down-outline", on_release=lambda x: self.rejectreq())
            reject_button.md_bg_color= 0.858, 0.239, 0.086, 1 #Red color
            self.ids['approval_float_lay'].add_widget(reject_button)
            
            self.ids['approval_float_lay'].add_widget(MDFillRoundFlatIconButton(text="BACK",
            pos_hint={'center_x':0.5, 'center_y':0.1}, icon="arrow-left-bold-circle",theme_text_color="Custom", 
            text_color= (0, 0, 1, 1), on_release=lambda x: self.to_home_page() ))

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        if current_row[0]+'|'+current_row[2] in self.conlist:
            self.conlist.remove(current_row[0]+'|'+current_row[2])
        else:
            self.conlist.append(current_row[0]+'|'+current_row[2])
        print(self.conlist)

    def approvereq(self):
        if(len(self.conlist)>0):
            for i in self.conlist:
                x = i.split("|")
                print(x[0], x[1])
                query = f'''UPDATE CONTACT_ORG SET STATUS='Y', MEMBER_FLAG='Y' 
                WHERE ORG_ID = (SELECT ORG_ID FROM ORG WHERE NAME = '{x[0]}')
                AND CONTACT_ID=(SELECT CONTACT_ID FROM CONTACT WHERE EMAIL='{x[1]}') '''
                # run direct SQL
                stmt = ibm_db.exec_immediate(connection.conn, query)
            self.manager.get_screen('approvals_window').load_approval_page()

    def rejectreq(self):
        if(len(self.conlist)>0):
            for i in self.conlist:
                x = i.split("|")
                print(x[0], x[1])
                query = f'''DELETE FROM CONTACT_ORG  
                WHERE ORG_ID = (SELECT ORG_ID FROM ORG WHERE NAME = '{x[0]}')
                AND CONTACT_ID=(SELECT CONTACT_ID FROM CONTACT WHERE EMAIL='{x[1]}') '''
                # run direct SQL
                stmt = ibm_db.exec_immediate(connection.conn, query)
            self.manager.get_screen('approvals_window').load_approval_page()

    def to_home_page(self):
        self.manager.current = 'home_window'
        self.manager.transition.direction = 'right'