import SwiftUI

struct SaloonDetailView: View {
    
    var sal_id : String
    
    @StateObject private var SaloonVM = SaloonViewModel()
    
    var body: some View {
        VStack {
            List(SaloonVM.singleSaloonData, id:\.id){ saloon in
                Text(saloon.name)
                    .font(.title)
                    .fontWeight(.bold)
                    .multilineTextAlignment(.center)
                    .padding()
                HStack{
                    Label("\(saloon.start_timings) - \(saloon.end_timings)", systemImage: "clock")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .padding(.trailing)
                }
                Text(saloon.description)
                    .font(.body)
                    .multilineTextAlignment(.leading)
                    .padding()
            }
            
            List(SaloonVM.serviceItems, id:\.id){ singleService in
                HStack{
                    VStack(alignment: .leading, spacing: 5){
                        Text(singleService.service_name)
                            .fontWeight(.bold)
                        Label("\(singleService.service_cost)", systemImage: "indianrupeesign.circle")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .padding(.trailing)
                        Label(singleService.service_duration, systemImage: "clock")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .padding(.trailing)
                    }.padding()
                    let defaults = UserDefaults.standard
                    if defaults.string(forKey: "jsonwebtoken") != nil {
                        NavigationLink(destination: BookingView(service_id: singleService.id, service_name: singleService.service_name, service_cost: singleService.service_cost, service_duration: singleService.service_duration), label: {Text("BOOK")})
                            .foregroundColor(Color.red)
                            .frame(width: 100, height: 30, alignment: .center)
                    }
                    else {
                        NavigationLink(destination: LoginView(), label: {Text("LOGIN")})
                            .foregroundColor(Color.red)
                            .frame(width: 100, height: 30, alignment: .center)
                    }
                }
            }.onAppear{
                SaloonVM.populateServiceItems(sal_id: sal_id)
                SaloonVM.getSingleSaloon(sal_id: sal_id)
            }
            Spacer()
        }
    }
}

