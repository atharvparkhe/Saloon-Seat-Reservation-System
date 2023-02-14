import SwiftUI

struct SaloonListView: View {
    
    @StateObject private var SaloonVM = SaloonViewModel()
    
    var body: some View {
        VStack{
            NavigationView{
                List(SaloonVM.saloonItems, id:\.id){ singleSaloon in
                    NavigationLink(destination: SaloonDetailView(sal_id: singleSaloon.id), label: {
                        HStack{
                            URLimage(url: "\(singleSaloon.logo)")
                                .frame(width:100, height: 100)
                                .cornerRadius(4.0)
                            VStack(alignment: .leading, spacing: 5){
                                Text(singleSaloon.name)
                                    .fontWeight(.bold)
                                    .lineLimit(2)
                                Text(singleSaloon.description)
                                    .fontWeight(.thin)
                                    .lineLimit(2)
                            }.padding()
                        }
                    })
                }
                .navigationTitle(Text("SALOON APP"))
                .onAppear{
                    SaloonVM.populateSaloonItems()
                }
            }
        }
    }
}
