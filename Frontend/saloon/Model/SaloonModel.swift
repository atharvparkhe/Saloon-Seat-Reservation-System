import Foundation


enum NetworkErrors: Error{
    case decodingError
    case badRequest
    case otherErrors(errorMessage: String)
}


struct MultiSaloon : Decodable{
    let id: String
    let name: String
    let description: String
    let logo: URL
}


struct Serivces: Decodable{
    let id: String
    let service_name: String
    let service_cost: Float
    let service_duration: String
}


struct SingleSaloon : Decodable{
    let id: String
    let name: String
    let description: String
    let logo: URL
    let seats: Int
    let latitude: Float
    let longitude: Float
    let rating: Float
    let start_timings: String
    let end_timings: String
}

//  View-Models

struct SaloonItemViewModel: Identifiable{
    
    private let saloon: MultiSaloon
    
    init(saloon:MultiSaloon){
        self.saloon = saloon
    }
    var id: String{
        saloon.id
    }
    var name: String{
        saloon.name
    }
    var description: String{
        saloon.description
    }
    var logo: URL{
        saloon.logo
    }
}


struct ServiceItemViewModel: Identifiable{
    
    private let services: Serivces
    
    init(services:Serivces){
        self.services = services
    }
    var id: String{
        services.id
    }
    var service_name: String{
        services.service_name
    }
    var service_cost: Float{
        services.service_cost
    }
    var service_duration: String{
        services.service_duration
    }
}


struct SingleSaloonViewModel: Identifiable{

    private let saloon: SingleSaloon

    init(saloon:SingleSaloon){
        self.saloon = saloon
    }
    var id: String{
        saloon.id
    }
    var name: String{
        saloon.name
    }
    var description: String{
        saloon.description
    }
    var logo: URL{
        saloon.logo
    }
    var longitude: Float{
        saloon.longitude
    }
    var latitude: Float{
        saloon.latitude
    }
    var rating: Float{
        saloon.rating
    }
    var start_timings: String{
        saloon.start_timings
    }
    var end_timings: String{
        saloon.end_timings
    }
}
