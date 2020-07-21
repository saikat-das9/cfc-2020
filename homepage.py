from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.list import MDList, TwoLineAvatarListItem, ImageLeftWidget
import connection
import ibm_db
import globalvariables
import os
from kivy.properties import ObjectProperty, StringProperty
from navdrawer import ContentNavigationDrawer
from activityhomepage import ActivityWindow
from kivy.metrics import dp

class HomeWindow(Screen):
    def load_home_page(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        self.load_org_list()

    # def test(args):
    #     print(args)

    def load_org_list(self):
        self.ids['scroll'].clear_widgets()      #To clear list of orgs
        query = f'''SELECT ORG_ID,NAME,REGISTRATION FROM ORG WHERE 
        ORG_ID IN (SELECT ORG_ID FROM CONTACT_ORG WHERE CONTACT_ID={globalvariables.var_userid} 
        AND MEMBER_FLAG='Y' AND STATUS='Y')'''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        orglist = ibm_db.fetch_both(stmt)
        item = TwoLineAvatarListItem()
        if orglist is False :
            self.ids['nogroupwarning'].pos_hint = {"x":0.2, "y":0.3}
            self.ids['nogroupwarning'].font_size = '10sp'
            self.ids['nogroupwarning'].text = "You have not joined any groups. Your joined groups will show up here"
            print("Hello")
            print(self.ids['nogroupwarning'].text)
        else:
            while (orglist):
                testid = orglist[1]
                if os.path.isfile('resources/org/'+str(orglist[0])+'.jpg'):  #To laod a default logo if logo not uploaded
                    image = ImageLeftWidget(source="resources/org/"+str(orglist[0])+".jpg")
                else:
                    image = ImageLeftWidget(source="resources/org/default.jpg")               
                item = TwoLineAvatarListItem(text=str(orglist[1]), secondary_text=str(orglist[2])  )
                item.add_widget(image)
                item.bind(on_release=self.row_press)
                self.ids['scroll'].add_widget(item)
                orglist = ibm_db.fetch_both(stmt)   #for incrementing rows inside while loop
    
    def row_press(self, instance_row):
        self.manager.current = 'activity_window'
        query = "SELECT ORG_ID FROM ORG WHERE REGISTRATION='"+instance_row.secondary_text+"'"
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        if userrow != False :
            globalvariables.var_org_id = userrow[0]
        self.manager.get_screen('activity_window').load_activity_page()
