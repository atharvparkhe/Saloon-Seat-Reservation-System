import SwiftUI

struct LoginView: View {
    
    @StateObject private var loginVM = LoginViewModel()
    
    var body: some View {
        VStack{
            NavigationView{
                Form{
                    TextField("Email", text: $loginVM.email)
                        .padding()
                    SecureField("Password", text: $loginVM.password)
                        .padding()
                    Button("LOGIN"){
                        print(loginVM.email)
                        print(loginVM.password)
                        loginVM.login()
                    }
                    .padding()
                    .frame(width: 120, height: 45, alignment: .center)
                }.navigationTitle("LOGIN")
            }
            let defaults = UserDefaults.standard
            if defaults.string(forKey: "jsonwebtoken") != nil {
                NavigationLink(destination: SaloonListView(), label: {Text("ALL SALOONS")})
                    .foregroundColor(Color.red)
                    .frame(width: 100, height: 30, alignment: .center)
            }
            Spacer()
            NavigationLink(destination: SignUpView(), label: {Text("SIGNUP")})
                .foregroundColor(Color.red)
                .frame(width: 100, height: 30, alignment: .center)
            NavigationLink(destination: ForgotView(), label: {Text("FORGOT")})
                .foregroundColor(Color.red)
                .frame(width: 100, height: 30, alignment: .center)
            Spacer()
        }
    }
}
