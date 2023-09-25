import time

token = r'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTU4MDYxOTUsImNpZCI6IjM2MzQ1NWRiZWQxZDVhMDQyNjQxN2JjMjE0N2ZjYjEzIn0.Y3QAd9MiKukrewOTcm3TbUnwHzTr-qNIIFHqu32A5wc'
row_count_per_page = 20
sleep_time = 60

# ==================================================
import requests
import spyder
import picklewa
import logwa

head = spyder.headers.default_headers()
head['Content-Type'] = 'application/json'
head['Token'] = token


def crawl_doc(page):
    data = {
        "method": "/basic/dangerRuleCount/searchSuperviseOrgPage",
        "reqType": "POST",
        "body": {
            "page": page,
            "rows": row_count_per_page,
            "orgName": "",
            "industryId": "0addb8ed-51cd-11e8-b241-6c92bf476c41",
            "businessScopeTypeId": "c7dff3dd-2952-11eb-8132-00ff88da4025,cbf562b6-2952-11eb-8132-00ff88da4025,70c4a8c9-5099-11eb-a7d6-00ff88da4025,cf57ef23-2952-11eb-8132-00ff88da4025,d2acf059-2952-11eb-8132-00ff88da4025,0436e249-5c80-11eb-a85b-0c42a1f2ce9c,117f9f33-5b12-11eb-a85b-0c42a1f2ce9c,83601147-5caf-11eb-86a5-54e1ad207ce0",
            "stat": 2,
            "orgStat": 1
        }
    }
    res = requests.post("https://dyg.ruoguinfo.cn:2517/dyg/req", headers=head, data=picklewa.json.dumps(data))
    return res


def crawl_people(page):
    data = {
        "method": "/dyg/dygRgEmp/getPageList",
        "reqType": "POST",
        "body": {
            "page": page,
            "rows": row_count_per_page,
            "industryId": "0addb8ed-51cd-11e8-b241-6c92bf476c41",
            "name": "",
            "ownerName": "",
            "mate": "",
            "stat": "",
            "businessScopeTypeId": "c7dff3dd-2952-11eb-8132-00ff88da4025,cbf562b6-2952-11eb-8132-00ff88da4025,70c4a8c9-5099-11eb-a7d6-00ff88da4025,cf57ef23-2952-11eb-8132-00ff88da4025,d2acf059-2952-11eb-8132-00ff88da4025,0436e249-5c80-11eb-a85b-0c42a1f2ce9c,117f9f33-5b12-11eb-a85b-0c42a1f2ce9c,83601147-5caf-11eb-86a5-54e1ad207ce0",
            "unfiled": 0
        }
    }
    res = requests.post("https://dyg.ruoguinfo.cn:2517/dyg/req", headers=head, data=picklewa.json.dumps(data))
    return res


def crawl_car(page):
    data = {
        "method": "/dyg/dygRgVeh/getPageList",
        "reqType": "POST",
        "body": {
            "page": page,
            "rows": row_count_per_page,
            "orgName": "",
            "industryId": "0addb8ed-51cd-11e8-b241-6c92bf476c41",
            "businessScopeTypeId": "c7dff3dd-2952-11eb-8132-00ff88da4025,cbf562b6-2952-11eb-8132-00ff88da4025,70c4a8c9-5099-11eb-a7d6-00ff88da4025,cf57ef23-2952-11eb-8132-00ff88da4025,d2acf059-2952-11eb-8132-00ff88da4025,0436e249-5c80-11eb-a85b-0c42a1f2ce9c,117f9f33-5b12-11eb-a85b-0c42a1f2ce9c,83601147-5caf-11eb-86a5-54e1ad207ce0",
            "stat": 2,
            "orgStat": 1
        }
    }
    res = requests.post("https://dyg.ruoguinfo.cn:2517/dyg/req", headers=head, data=picklewa.json.dumps(data))
    return res


def handle_res(data, last_page, last_index):
    data = picklewa.json.loads(data.text)['data']['rows']
    res = []

    for row in range(0, len(data)):
        if last_index < row:
            last_index = row
            res.append(data[row])
    if len(data) == row_count_per_page:
        return res, last_page + 1, -1
    else:
        return res, last_page, last_index


def main():
    logwa.line()
    logwa.info("Start crawling")
    f_doc = open('业户档案.txt', 'a',encoding='utf8')
    f_people = open('备案人员.txt', 'a',encoding='utf8')
    f_car = open('备案车辆.txt', 'a',encoding='utf8')
    last_doc_page, last_people_page, last_car_page = 1, 1, 1
    last_doc_index, last_people_index, last_car_index = -1, -1, -1

    try:
        last_doc_page, last_people_page, last_car_page, last_doc_index, last_people_index, last_car_index = picklewa.file.load_all(
            'pickle.pck')
        logwa.infof("{::gx} to load data from picklewa.pck", "Success")
    except FileNotFoundError:
        logwa.warnf("{::rx} to load data from picklewa.pck, use default value", "Failed")

    try:
        while True:
            logwa.infof("Crawling doc page {::ux}", last_doc_page)
            res, last_doc_page, last_doc_index = handle_res(crawl_doc(last_doc_page), last_doc_page, last_doc_index)
            logwa.infof("Get rows : {::ux}", len(res))
            for row in res:
                f_doc.write(picklewa.json.dumps(row) + '\n')

            logwa.infof("Crawling people page {::ux}", last_people_page)
            res, last_people_page, last_people_index = handle_res(crawl_people(last_people_page), last_people_page,
                                                                  last_people_index)
            logwa.infof("Get rows : {::ux}", len(res))
            for row in res:
                f_people.write(picklewa.json.dumps(row) + '\n')

            logwa.infof("Crawling car page {::ux}", last_car_page)
            res, last_car_page, last_car_index = handle_res(crawl_car(last_car_page), last_car_page,
                                                            last_car_index)
            logwa.infof("Get rows : {::ux}", len(res))
            for row in res:
                f_car.write(picklewa.json.dumps(row) + '\n')

            time.sleep(sleep_time)
    except KeyboardInterrupt:
        f_doc.close()
        f_people.close()
        f_car.close()
        picklewa.file.dump_all('pickle.pck', last_doc_page, last_people_page, last_car_page, last_doc_index,
                               last_people_index,
                               last_car_index)
        logwa.infof("User keyboard interrupt, data save as {::ux},{::ux},{::ux}",
                    '业户档案.txt',
                    '备案人员.txt',
                    '备案车辆.txt')


if __name__ == '__main__':
    main()
