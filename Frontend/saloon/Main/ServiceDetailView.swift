//
//  ServiceDetailView.swift
//  saloon
//
//  Created by Atharva Parkhe on 13/02/22.
//

import SwiftUI

struct ServiceDetailView: View {
    
    var singleService : Serivces
    
    var body: some View {
        VStack{
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
            Button("BOOK NOW"){
                print("Button clicked : \(singleService.id)")
            }
            .frame(width: 120, height: 45, alignment: .center)
            .foregroundColor(Color.red)
        }
    }
}

struct ServiceDetailView_Previews: PreviewProvider {
    static var previews: some View {
        ServiceDetailView()
    }
}
