import Foundation
import CoreImage

enum AuthenticationError: Error {
    case CustomError(errorMessage:String)
}

struct LoginRequestBody: Codable{
    let email : String
    let password : String
}

struct LoginResponse: Codable{
    let message : String
    let token : String
}

struct SignupRequestBody: Codable {
    let name : String
    let email : String
    let password : String
}

struct ForgotBodyRequest: Codable {
    let email : String
}
