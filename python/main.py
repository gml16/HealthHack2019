from processor import process_image


def main():
    gums = "../diagnostic_uploads/cancer1.png"
    cancer = process_image(gums, "gums")

    tongue_ulcer = "../diagnostic_uploads/syphilis2.png"
    syphilis_1 = process_image(tongue_ulcer, "tongue_ulcer")

    tongue_patch = "../diagnostic_uploads/syphilis3.png"
    syphilis_2 = process_image(tongue_patch, "tongue_patch")

    lips = "../diagnostic_uploads/herpes4.png"
    herpes = process_image(lips, "lips")
    print(res)

if __name__ == "__main__":
    main()
