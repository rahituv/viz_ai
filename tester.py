import requests

r = requests.post("http://localhost:8080/best_most_common_face", json={
    "image_name_list": ["none_face.jpg"]
})

print r.status_code
print r.text

r = requests.post("http://localhost:8080/best_most_common_face", json={
    "image_name_list": []
})

print r.status_code
print r.text

r = requests.post("http://localhost:8080/best_most_common_face", json={
})

print r.status_code
print r.text

r = requests.post("http://localhost:8080/best_most_common_face", json={
    "image_name_list": ["k1.jpg", "l2.jpg", "l3.jpg", "l4.jpg",
                                                                 "l5.jpg", "l6.jpg", "l7.jpg"]
})

print r.status_code
print r.text

r = requests.post("http://localhost:8080/best_most_common_face", json={
    "image_name_list": ["l1.jpg", "l2.jpg", "l3.jpg", "l4.jpg",
                                                                 "l5.jpg", "l6.jpg", "l7.jpg"]
})

print r.status_code
print r.text
