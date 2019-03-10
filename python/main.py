from processor import process_image


def main():

    lips = "../diagnostic_uploads/herpes4.png"
    tongue_ulcer = "../diagnostic_uploads/syphilis2.png"
    tongue_patch = "../diagnostic_uploads/syphilis3.png"
    gums = "../diagnostic_uploads/cancer1.png"

    files = [lips, tongue_ulcer, tongue_patch, gums]

    print(process_image(files))

if __name__ == "__main__":
    main()
