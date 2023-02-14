import Foundation


class SaloonViewModel: ObservableObject {
    
    @Published var saloonItems = [SaloonItemViewModel]()
    
    @Published var serviceItems = [ServiceItemViewModel]()
    
    @Published var singleSaloonData = [SingleSaloonViewModel]()
    
    func populateSaloonItems(){
        SaloonWebServices().getAllSaloons() { result in
            switch result{
                case .success(let saloons):
                DispatchQueue.main.async {
                    self.saloonItems = saloons.map(SaloonItemViewModel.init)
                }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    func populateServiceItems(sal_id: String){
        SaloonWebServices().getAllServices(sal_id: sal_id) { result in
            switch result{
                case .success(let services):
                    DispatchQueue.main.async {
                        self.serviceItems = services.map(ServiceItemViewModel.init)
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
    
    func getSingleSaloon(sal_id: String){
        SaloonWebServices().getSingleSaloons(sal_id: sal_id) { result in
            switch result{
                case .success(let saloonData):
                    DispatchQueue.main.async {
                        self.singleSaloonData = saloonData.map(SingleSaloonViewModel.init)
                    }
                case .failure(let error):
                    print(error.localizedDescription)
            }
        }
    }
}
