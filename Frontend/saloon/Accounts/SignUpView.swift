import SwiftUI

struct SignUpView: View {
    
    @StateObject private var signupVM = SignupViewModel()
    
    var body: some View {
        VStack{
            NavigationView{
                Form{
                    TextField("Name", text: $signupVM.name)
                        .padding()
                    TextField("Email", text: $signupVM.email)
                        .padding()
                    SecureField("Password", text: $signupVM.password)
                        .padding()
                    Button("SIGNUP"){
                        print(signupVM.email)
                        print(signupVM.password)
                        signupVM.signup()
                    }
                    .padding()
                    .frame(width: 120, height: 45, alignment: .center)
                }.navigationTitle("SIGNUP")
            }
            Spacer()
            NavigationLink(destination: LoginView(), label: {Text("LOGIN")})
                .foregroundColor(Color.red)
                .frame(width: 100, height: 30, alignment: .center)
            NavigationLink(destination: ForgotView(), label: {Text("FORGOT")})
                .foregroundColor(Color.red)
                .frame(width: 100, height: 30, alignment: .center)
            Spacer()
        }
    }
}
