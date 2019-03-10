//
//  MorePicsViewController.swift
//  HealthHack19
//
//  Created by Samuel Martin on 10/03/2019.
//  Copyright © 2019 Samuel Martin. All rights reserved.
//

import UIKit
import Foundation
import Photos

class MorePicsViewController: UIViewController,UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    //Variables
    var imageGums: UIImage?
    var imageLips: UIImage?
    var lipsSelected: Bool = false
    var gumsSelected: Bool = false
    let picker = UIImagePickerController()
    
    
    //Outlets
    @IBOutlet weak var lipsImg: UIImageView!
    @IBOutlet weak var gumsImg: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupView()
        
        // Do any additional setup after loading the view.
    }
    
    override func viewDidAppear(_ animated: Bool) {
        picker.delegate = self
        picker.allowsEditing = true
        picker.sourceType = .photoLibrary
    }
    
    @IBAction func backBtnPressed(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
    }
    @IBAction func uploadPicturesPressed(_ sender: Any) {
    }
    
    @IBAction func gumsBtnPressed(_ sender: Any) {
        self.gumsSelected = true
        let logoutPopup = UIAlertController(title: "Choose source", message:
            nil, preferredStyle: .actionSheet)
        let PictureUpload = UIAlertAction(title: "Select Picture", style: .default) { (buttonTapped) in
            self.checkLibraryPermission()
        }
        let CancelAction = UIAlertAction(title: "Cancel", style: .cancel, handler: nil)
        let TakePicture = UIAlertAction(title: "Take Picture", style: .default) { (buttonTapped) in
            self.checkPermission()
        }
        
        logoutPopup.addAction(CancelAction)
        logoutPopup.addAction(PictureUpload)
        logoutPopup.addAction(TakePicture)
        present(logoutPopup, animated: true, completion: nil)
        
    }
    
    
    @IBAction func lipsBtnPressed(_ sender: Any) {
        self.lipsSelected = true
        let logoutPopup = UIAlertController(title: "Choose source", message:
            nil, preferredStyle: .actionSheet)
        let PictureUpload = UIAlertAction(title: "Select Picture", style: .default) { (buttonTapped) in
            self.checkLibraryPermission()
        }
        let CancelAction = UIAlertAction(title: "Cancel", style: .cancel, handler: nil)
        let TakePicture = UIAlertAction(title: "Take Picture", style: .default) { (buttonTapped) in
            self.checkPermission()
        }
        
        logoutPopup.addAction(CancelAction)
        logoutPopup.addAction(PictureUpload)
        logoutPopup.addAction(TakePicture)
        present(logoutPopup, animated: true, completion: nil)
    }
    
    
    func setupView() {
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(ImageUploadVC.handleTap))
        view.addGestureRecognizer(tap)
    }
    
    func camera()
    {
        if UIImagePickerController.isSourceTypeAvailable(.camera){
            let myPickerController = UIImagePickerController()
            myPickerController.delegate = self;
            myPickerController.sourceType = .camera
            myPickerController.allowsEditing = false
            self.present(myPickerController, animated: true, completion: nil)
        }
        
    }
    
    func photoLibrary()
    {
        
        if UIImagePickerController.isSourceTypeAvailable(.photoLibrary){
            let myPickerController = UIImagePickerController()
            myPickerController.delegate = self;
            myPickerController.sourceType = .photoLibrary
            myPickerController.allowsEditing = true
            self.present(myPickerController, animated: true, completion: nil)
        }
    }
    
    @objc func handleTap(){
        view.endEditing(true)
    }
    
    @objc internal func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        
        var selectedImage: UIImage?
        if let editedImage = info["UIImagePickerControllerEditedImage"] as? UIImage{
            selectedImage = editedImage
        }else if let originalImage = info["UIImagePickerControllerOriginalImage"] as? UIImage{
            selectedImage = originalImage
        }
        
        if let selImage = selectedImage{
            if self.lipsSelected{
                lipsImg.contentMode = .scaleAspectFill
                lipsImg.image = selImage
                imageLips = selImage
                IMAGE_LIPS = selImage
                lipsSelected = false
            } else if self.gumsSelected{
                gumsImg.contentMode = .scaleAspectFill
                gumsImg.image = selImage
                imageGums = selImage
                IMAGE_GUMS = selImage
                gumsSelected = false
            }
        } else {
            print("nil IMage found")
        }
        
        dismiss(animated: true, completion: nil)
    }
    
    func checkPermission(){
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized: // The user has previously granted access to the camera.
            self.camera()
            
        case .notDetermined: // The user has not yet been asked for camera access.
            AVCaptureDevice.requestAccess(for: .video) { granted in
                if granted {
                    self.camera()
                }
            }
            
        case .denied: // The user has previously denied access.
            return
        case .restricted: // The user can't grant access due to restrictions.
            return
        }
    }
    
    func checkLibraryPermission() {
        let photoAuthorizationStatus = PHPhotoLibrary.authorizationStatus()
        switch photoAuthorizationStatus{
        case .authorized:
            print("Access is granted by user")
            photoLibrary()
        case .notDetermined: PHPhotoLibrary.requestAuthorization({
            (newStatus) in print("status is \(newStatus)")
            if newStatus == PHAuthorizationStatus.authorized
            {
                print("success")
                self.photoLibrary()
            }
        })
        case .restricted: print("User do not have access to photo album.")
            return
        case .denied: print("User has denied the permission.")
            return
        }
    }

}
