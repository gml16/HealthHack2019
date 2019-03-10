//
//  CreateAccountVC.swift
//  Smack
//
//  Created by Samuel Martin on 20/10/2017.
//

import UIKit
import Foundation
import AVFoundation
import Photos


class ImageUploadVC: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    //Outlets
    @IBOutlet weak var ageTxtField: UITextField!
    @IBOutlet weak var genderTxtField: UITextField!
    @IBOutlet weak var otherTxtField: UITextField!
    @IBOutlet weak var userImage: UIImageView!
    @IBOutlet weak var UploadHHBtn: RoundedButton!
    
    
    
    
    
    //Variables
    var image: UIImage?
    let picker = UIImagePickerController()
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupView()
    }
    
    override func viewDidAppear(_ animated: Bool) {
        picker.delegate = self
        picker.allowsEditing = true
        picker.sourceType = .photoLibrary
    }
    
    
    @IBAction func chooseImagePressed(_ sender: Any) {
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
    
    @IBAction func UploadImagesPressed(_ sender: Any) {
        if image != nil{
            if let vc = self.storyboard?.instantiateViewController(withIdentifier: "PicturesVC") as! MorePicsViewController? {
            self.present(vc, animated: true, completion: nil)
            }
        }
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
    
    @objc func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        
        var selectedImage: UIImage?
        if let editedImage = info["UIImagePickerControllerEditedImage"] as? UIImage{
            selectedImage = editedImage
        }else if let originalImage = info["UIImagePickerControllerOriginalImage"] as? UIImage{
            selectedImage = originalImage
        }
        
        if let selImage = selectedImage{
            userImage.contentMode = .scaleAspectFill
            userImage.image = selImage
            image = selImage
            IMAGE_TOUNGE = selImage
        } else {
            self.userImage.backgroundColor = #colorLiteral(red: 0.4784313725, green: 0.5058823529, blue: 1, alpha: 1)
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
