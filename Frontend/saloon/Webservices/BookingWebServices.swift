import Foundation


class BookingWebservices{
    
    func makeBookingWebService(service_id: String, date: String, token: String, completion: @escaping (Result<String, AuthenticationError>) -> Void ){
        guard let url = URL(string: "\(Constants.BASE_API_URL)make-booking/") else {
            completion(.failure(.CustomError(errorMessage: "Invalid URL")))
            return
        }
        let body = BookingRequestBody(service_id: service_id, date: date)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.httpBody = try? JSONEncoder().encode(body)
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data=data, error == nil else{
                completion(.failure(.CustomError(errorMessage: "No Data")))
                return
            }
            guard let MessageResponse = try? JSONDecoder().decode(MessageResponse.self, from: data) else{
                completion(.failure(.CustomError(errorMessage: "Invalid data passed")))
                return
           }
            completion(.success(MessageResponse.message))
        }.resume()
    }
}
