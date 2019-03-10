//
//  serverDiscussion.swift
//  HealthHack19
//
//  Created by Rémi Uzel on 10/03/2019.
//  Copyright © 2019 Samuel Martin. All rights reserved.
//

import Foundation
import UIKit

func uploadImage(image: UIImage) -> Void{
    //Convert the image to a data blob
    guard let png = image.pngData() else{
        print("Image must be png format.")
        return
    }
    
    //Set up a network request
    let request = NSMutableURLRequest()
    request.httpMethod = "POST"
    request.url = URL(string: "http://127.0.0.1:5000/")
    request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
    request.setValue("\(png.count)", forHTTPHeaderField: "Content-Length")
    request.httpBody = png
    // Figure out what the request is making and the encoding type...
    
    //Execute the network request
    let upload = URLSession.shared.uploadTask(with: request as URLRequest, from: png, completionHandler: {(data: Data?, response: URLResponse?, error: Error?) -> Void in
        if (error != nil) {
            print("Error: \(String(describing: error))")
        } else {
            let outputstr = String(data: data!, encoding: String.Encoding.utf8) as! String
            print(outputstr)
            // TODO: Do something with the respose data - i.e. decision tree for questions.
        }
    })

    
    upload.resume()
    
}
