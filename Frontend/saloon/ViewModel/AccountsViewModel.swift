import Foundation

class LoginViewModel: ObservableObject {
    
    var email : String = ""
    var password : String = ""
    
    func login(){
        
        let defaults = UserDefaults.standard
        
        AccountWebservices().login(email: email, password: password) { result in
            switch result{
                case .success(let token):
                defaults.setValue(token, forKey: "jsonwebtoken")
                case.failure(let error):
                    print(error.localizedDescription)
                }
        }
    }
}


class SignupViewModel: ObservableObject {
    
    var name : String = ""
    var email : String = ""
    var password : String = ""
    
    func signup(){
        
        AccountWebservices().signup(name: name, email: email, password: password) { result in
            switch result{
                case .success(let message):
                    print(message)
                case.failure(let error):
                    print(error.localizedDescription)
                }
        }
    }
    
}

class ForgotViewModel : ObservableObject {
    
    var email : String = ""
    
    func forgot(){
        
        AccountWebservices().forgot(email: email) { result in
            switch result{
                case .success(let message):
                    print(message)
                case.failure(let error):
                    print(error.localizedDescription)
                }
        }
    }
}
