from processor import process_image


def main():
    filename = "../diagnostic_uploads/herpes1.PNG"
    res = process_image(filename)
    print(res)

if __name__ == "__main__":
    main()
