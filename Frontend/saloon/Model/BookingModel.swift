import Foundation


struct BookingRequestBody: Codable{
    let service_id : String
    let date : String
}

struct MessageResponse: Codable{
    let message: String
}
