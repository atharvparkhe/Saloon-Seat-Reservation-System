//
//  URLimage.swift
//  saloon
//
//  Created by Atharva Parkhe on 13/02/22.
//

import SwiftUI

struct URLimage: View {
    
    let url: String
    let placeholder: String

    @ObservedObject var imageLoader = ImageLoader()

    init (url: String, placeholder: String = "placeholder") {
        self.url = url
        self.placeholder = placeholder
        self.imageLoader.downloadImage(url:self.url)
    }

    var body: some View {
        
        if let data = self.imageLoader.downloadedData {
            return Image(uiImage: UIImage (data: data)!).renderingMode(.original).resizable()
        } else {
            return Image("placeholder").renderingMode(.original).resizable()
        }

    }
}

struct URLimage_Previews: PreviewProvider {
    static var previews: some View {
        URLimage (url: "https://fyrafix.files.wordpress.com/2011/08/url-8.jpg")
    }
}
