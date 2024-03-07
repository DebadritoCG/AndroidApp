import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from jnius import autoclass
from jnius import cast
from threading import Thread

sess = requests.session()
def get_value():
    get_url = 'http://192.168.29.122:5000/get'
    get_params = {'key': 'name'}
    response = sess.get(get_url, params=get_params)
    return response.json()

class ConnectorApp(App):
    server_ip = "192.168.29.122"
    server_port = 5000
    base_url = f"http://{server_ip}:{str(server_port)}"

    def set_phone_number_value(self, instace):
        def action():
            while True:
                obj = get_value()
                if "value" in dict(obj).keys():
                    phone_no = obj['value']
                    self._call(str(phone_no))
        
        th = Thread(target=action)
        th.start()

    
    def _call(self, phone_no):
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        PythonActivity = autoclass('org.renpy.android.PythonActivity') 
        intent = Intent(Intent.ACTION_CALL)
        intent.setData(Uri.parse("tel:" + str(phone_no)))
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)
        self.set_phone_number_value()

    def build(self):
        layout = BoxLayout(orientation="vertical")
        self.label = Label(text="Not connected")
        layout.add_widget(self.label)
        connect_button = Button(text="Connect")
        connect_button.bind(on_press=self.set_phone_number_value)
        layout.add_widget(connect_button)
        return layout

if __name__ == "__main__":
    ConnectorApp().run()

# Set a value
# def set_value(key, value):
#     set_url = 'http://192.168.29.122:5000/set'
#     set_data = {'key': key, 'value': value}
#     response = sess.post(set_url, json=set_data)
#     return response.json()

# Get a value
        


def call(name,phone):
    #TODO
    ...
