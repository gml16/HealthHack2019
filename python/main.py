from processor import process_image


def main():
    gums = "../diagnostic_uploads/cancer1.png"
    cancer = process_image(gums, "gums")

    tongue = "../diagnostic_uploads/syphilis3.png"
    syphilis = process_image(tongue, "tongue")

    lips = "../diagnostic_uploads/herpes4.png"
    herpes = process_image(lips, "lips")
    print(res)

if __name__ == "__main__":
    main()
