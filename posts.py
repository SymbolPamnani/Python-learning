import pandas as pd

posts = [
    {"post_id": 1, "content": "Hello world!", "likes": 150, "comments": 12, "shares": 5, "views": 1000},
    {"post_id": 2, "content": "Python is awesome", "likes": 320, "comments": 28, "shares": 15, "views": 2500},
    {"post_id": 3, "content": "Check out my new project!", "likes": 450, "comments": 45, "shares": 30, "views": 3000},
    {"post_id": 4, "content": "Weekend vibes", "likes": 280, "comments": 18, "shares": 8, "views": 1800},
    {"post_id": 5, "content": "Amazing sunset", "likes": 520, "comments": 32, "shares": 22, "views": 3500},
    {"post_id": 6, "content": "Learning data science", "likes": 190, "comments": 15, "shares": 10, "views": 1500},
    {"post_id": 7, "content": "New blog post", "likes": 380, "comments": 25, "shares": 18, "views": 2200},
    {"post_id": 8, "content": "Product launch!", "likes": 680, "comments": 55, "shares": 45, "views": 4500},
    {"post_id": 9, "content": "Throwback Thursday", "likes": 210, "comments": 14, "shares": 7, "views": 1200},
    {"post_id": 10, "content": "Thank you followers!", "likes": 430, "comments": 38, "shares": 25, "views": 2800},
]


for p in posts:
    p['erate'] = (p['likes'] + p['comments']*2 + p['shares']*3 / p['views'])

for p in posts:
    print(p['content'], p["erate"])

e_rate = [(p['post_id'], p['erate']) for p in posts]
print("________List________")
print(e_rate)

p_sorted = sorted(posts, key=lambda x:x["likes"], reverse=True)
top3 = p_sorted[:3]   # slicing
print(top3)

p = pd.DataFrame(posts)

def checkcat(row):
    if row['erate'] <= 100:
        return "Low engagement"
    elif row['erate'] <= 400:
        return "Medium"
    else:
        return "High engagement"

p['category'] = p.apply(checkcat, axis=1)

print(p[['content', 'erate', 'category']])

avglikes= sum(p['likes'])// len(p)
avgcom= sum(p['comments'])// len(p)
avgsha= sum(p['shares'])// len(p)

newtup=(avglikes, avgcom, avgsha)
print(newtup)

if avgcom > avgsha:
    print("More comments")
elif avgcom < avgsha:
    print("More shares")
else:
    print("Both are equal")

for i in range(len(p)):
    p.loc[i, 'likes'] += 10
    p.loc[i, 'comments'] += 5
    p.loc[i, 'shares'] += 2

print(p[['likes', 'comments', 'shares']])