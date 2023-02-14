import Foundation


class BookingViewModel: ObservableObject {
    
    @Published var mess = ""
    
    func makeBooking(ser_id: String, date: String){
        
        let defaults = UserDefaults.standard
        guard let token = defaults.string(forKey: "jsonwebtoken") else {
            return
        }
        
        BookingWebservices().makeBookingWebService(service_id: ser_id, date: date, token: token){ result in
            switch result{
            case .success(let resp):
                DispatchQueue.main.async {
                    self.mess = resp
                }
            case .failure(let error):
                print(error.localizedDescription)
            }
        }
    }
}
