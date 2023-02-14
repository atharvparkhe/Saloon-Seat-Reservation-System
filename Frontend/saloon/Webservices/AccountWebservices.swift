import Foundation


class AccountWebservices{
    
    func login(email: String, password: String, completion: @escaping (Result<String, AuthenticationError>) -> Void ){
        guard let url = URL(string: "\(Constants.BASE_API_URL)login/") else {
            completion(.failure(.CustomError(errorMessage: "Invalid URL")))
            return
        }
        let body = LoginRequestBody(email: email, password: password)
        var request = URLRequest(url: url)
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("application/json", forHTTPHeaderField: "Accept")
        request.httpMethod = "POST"
        request.httpBody = try? JSONEncoder().encode(body)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data=data, error == nil else{
                completion(.failure(.CustomError(errorMessage: "No Data")))
                return
            }
            guard let LoginResponse = try? JSONDecoder().decode(LoginResponse.self, from: data) else{
                completion(.failure(.CustomError(errorMessage: "Invalid Credentials")))
                return
           }
            completion(.success(LoginResponse.token))
        }.resume()
        
    }

    
    func signup(name: String, email: String, password: String, completion: @escaping (Result<String, AuthenticationError>) -> Void ){
        guard let url = URL(string: "\(Constants.BASE_API_URL)signup/") else {
            completion(.failure(.CustomError(errorMessage: "Invalid URL")))
            return
        }
        let body = SignupRequestBody(name: name, email: email, password: password)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONEncoder().encode(body)
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data=data, error == nil else{
                completion(.failure(.CustomError(errorMessage: "No Data")))
                return
            }
            guard let MessageResponse = try? JSONDecoder().decode(MessageResponse.self, from: data) else{
                completion(.failure(.CustomError(errorMessage: "Account Already Exist")))
                return
           }
            completion(.success(MessageResponse.message))
        }.resume()
    }
    
    
    func forgot(email: String, completion: @escaping (Result<String, AuthenticationError>) -> Void ){
        guard let url = URL(string: "\(Constants.BASE_API_URL)forgot/") else {
            completion(.failure(.CustomError(errorMessage: "Invalid URL")))
            return
        }
        let body = ForgotBodyRequest(email: email)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONEncoder().encode(body)
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data=data, error == nil else{
                completion(.failure(.CustomError(errorMessage: "No Data")))
                return
            }
            guard let MessageResponse = try? JSONDecoder().decode(MessageResponse.self, from: data) else{
                completion(.failure(.CustomError(errorMessage: "Account Does Not Exist. Please Signup")))
                return
           }
            completion(.success(MessageResponse.message))
        }.resume()
    }
}
