from processor import process_image


def main():
    gums = "../diagnostic_uploads/cancer1.png"
    cancer = process_image(gums, "gums")

    tongue_ulcer = "../diagnostic_uploads/syphilis2.png"
    # TODO - DETECT OVAL INSTEAD OF APPLYING MASK
    syphilis_1 = process_image(tongue_ulcer, "tongue_ulcer") 

    tongue_patch = "../diagnostic_uploads/syphilis1.png"
    syphilis_2 = process_image(tongue_patch, "tongue_patch")

    lips = "../diagnostic_uploads/herpes4.png"
    # TODO - DETECT OVAL INSTEAD OF APPLYING MASK
    herpes = process_image(lips, "lips") 


if __name__ == "__main__":
    main()
