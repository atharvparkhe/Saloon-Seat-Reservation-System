import SwiftUI

struct BookingView: View {
    
    @StateObject private var BookingVM = BookingViewModel()
    
    @State private var date = Date()
    
    var service_id : String
    var service_name : String
    var service_cost : Float
    var service_duration : String
    
    var body: some View {
        
        VStack(alignment: .leading, spacing: 15) {
            Text(service_name)
                .fontWeight(.bold)
            Label("\(service_cost)", systemImage: "indianrupeesign.circle")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .padding(.trailing)
            Label(service_duration, systemImage: "clock")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .padding(.trailing)
            Spacer()
            if BookingVM.mess != "" {
                Text("\(BookingVM.mess)")
                    .bold()
                    .frame(width: 200, height: 200, alignment: .center)
                NavigationLink(destination: SaloonListView(), label: {Text("All Saloons")})
                    .foregroundColor(Color.red)
                    .frame(width: 100, height: 50, alignment: .center)
            }
            Form{
                DatePicker("Select Reservation Date : ", selection: $date, displayedComponents: .date)
            }
            HStack(alignment: .center, spacing: 5) {
                Button("BOOK NOW"){
                    let dateFormatter = DateFormatter()
                    dateFormatter.dateFormat = "yyyy-MM-dd"
                    let dateString = dateFormatter.string(from: date)
                    BookingVM.makeBooking(ser_id: service_id, date: dateString)
                }
                .frame(width: 120, height: 45, alignment: .center)
                .foregroundColor(Color.red)
            }
        }.padding()
    }
}
