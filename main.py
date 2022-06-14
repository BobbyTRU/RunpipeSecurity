import warnIssueSummarizer
import sqlConnection
import downloader


def main():
    dif, appCounter = downloader.downloadApps()
    dif += warnIssueSummarizer.summarize()
    dif += sqlConnection.writeToDB()
    avgTime = dif/appCounter
    print("total time spent:",dif)
    print("avg time per app:",avgTime)


main()