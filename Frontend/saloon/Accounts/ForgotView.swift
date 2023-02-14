import SwiftUI

struct ForgotView: View {
    
    @StateObject private var forgotVM = ForgotViewModel()
    
    var body: some View {
        VStack{
            NavigationView{
                Form{
                    TextField("Email", text: $forgotVM.email)
                        .padding()
                    Button("RESET PASSWORD"){
                        print(forgotVM.email)
                        forgotVM.forgot()
                    }
                    .padding()
                    .frame(width: 120, height: 45, alignment: .center)
                }.navigationTitle("RESET")
            }
            Spacer()
            NavigationLink(destination: LoginView(), label: {Text("LOGIN")})
                .foregroundColor(Color.red)
                .frame(width: 100, height: 30, alignment: .center)
            NavigationLink(destination: SignUpView(), label: {Text("SIGNUP")})
                .foregroundColor(Color.red)
                .frame(width: 100, height: 30, alignment: .center)
            Spacer()
        }
    }
}
