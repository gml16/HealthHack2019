from processor import process_image


def main():
    filename = "../diagnostic_uploads/syphilis3.png"
    res = process_image(filename)
    print(res)

if __name__ == "__main__":
    main()
