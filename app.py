from service import TheFlashServer

if __name__ == "__main__":
    service = TheFlashServer(debug=True)
    service.start()
