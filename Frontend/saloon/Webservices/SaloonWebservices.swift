import Foundation

//func getSingleSaloonData(){
//    var singleSaloonData : SingleSaloon
//
//    let urlString = "http://taco-randomizer.herokuapp.com/random/"
//    let url = URL (string: urlString)
//    URLSession.shared.dataTask(with: url!) {data, _, error in
//        if let data = data {
//            do{
//                let decodedData = try JSONDecoder().decode(singleSaloonData.self, from: data)
//                singleSaloonData = decodedData
//            } catch {
//                print ("Error! Something went wrong")
//            }
//        }
//    }
//}


class SaloonWebServices{
    
    func getAllSaloons(completion: @escaping (Result<[MultiSaloon], NetworkErrors>) -> Void){
        guard let url = URL(string: "\(Constants.BASE_API_URL)saloons/") else {
            completion(.failure(.otherErrors(errorMessage: "Incorrect URL")))
            return
        }
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data=data, error == nil, (response as? HTTPURLResponse)?.statusCode == 200 else{
                completion(.failure(.badRequest))
                return
            }
            let saloons = try?  JSONDecoder().decode([MultiSaloon].self, from: data)
            completion(.success(saloons ?? []))
        }.resume()
    }
    
    
    func getSingleSaloons(sal_id: String, completion: @escaping (Result<[SingleSaloon], NetworkErrors>) -> Void){
        guard let url = URL(string: "\(Constants.BASE_API_URL)saloon/\(sal_id)/") else {
            completion(.failure(.otherErrors(errorMessage: "Incorrect URL")))
            return
        }
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data=data, error == nil, (response as? HTTPURLResponse)?.statusCode == 200 else{
                completion(.failure(.badRequest))
                return
            }
            let saloonData = try?  JSONDecoder().decode([SingleSaloon].self, from: data)
            completion(.success(saloonData ?? []))
        }.resume()
    }
    
    
    
    func getAllServices(sal_id: String, completion: @escaping (Result<[Serivces], NetworkErrors>) -> Void){
        guard let url = URL(string: "\(Constants.BASE_API_URL)get-services/\(sal_id)/") else {
            completion(.failure(.otherErrors(errorMessage: "Incorrect URL")))
            return
        }
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data=data, error == nil, (response as? HTTPURLResponse)?.statusCode == 200 else{
                completion(.failure(.badRequest))
                return
            }
            let services = try?  JSONDecoder().decode([Serivces].self, from: data)
            completion(.success(services ?? []))
        }.resume()
    }
    
    
    
    func getSingleService(ser_id: String, completion: @escaping (Result<Serivces, NetworkErrors>) -> Void){
        guard let url = URL(string: "\(Constants.BASE_API_URL)service/\(ser_id)/") else {
            completion(.failure(.otherErrors(errorMessage: "Incorrect URL")))
            return
        }
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data=data, error == nil, (response as? HTTPURLResponse)?.statusCode == 200 else{
                completion(.failure(.badRequest))
                return
            }
            let serviceData = try?  JSONDecoder().decode(Serivces.self, from: data)
            completion(.success(serviceData.unsafelyUnwrapped))
        }.resume()
    }
}
