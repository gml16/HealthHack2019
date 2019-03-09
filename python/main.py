from processor import process_image


def main():
    filename = "../diagnostic_uploads/test_guy_mouth.PNG"
    res = process_image(filename)
    print(res)

if __name__ == "__main__":
    main()
