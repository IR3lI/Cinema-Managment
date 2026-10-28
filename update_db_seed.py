import sqlite3, sys, uuid, datetime

sys.stdout.reconfigure(encoding='utf-8')
db_path = 'publish/app.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Update Movie Posters
for i in range(1, 16):
    cur.execute('UPDATE Movies SET PosterUrl = ? WHERE MovieId = ?', (f'/uploads/posters/poster_{i}.jpg', i))
print('Updated 15 Movie posters!')

# 2. Update FoodItem Images
for i in range(1, 15):
    cur.execute('UPDATE FoodItems SET ImageUrl = ? WHERE FoodItemId = ?', (f'/uploads/fnb/fnb_{i}.jpg', i))
print('Updated 14 FoodItem images!')

# 3. Ensure Customer Users
new_users = [
    ('vuthimai@gmail.com', 'Vũ Thị Mai', '0936666777'),
    ('doquanghuy@gmail.com', 'Đỗ Quang Huy', '0945555888'),
    ('buithutrang@gmail.com', 'Bùi Thu Trang', '0923333999'),
    ('nguyenphuctien@gmail.com', 'Nguyễn Phúc Tiến', '0918888111')
]

for email, name, phone in new_users:
    cur.execute('SELECT Id FROM AspNetUsers WHERE Email = ?', (email,))
    row = cur.fetchone()
    if not row:
        u_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute('''
            INSERT INTO AspNetUsers (Id, UserName, NormalizedUserName, Email, NormalizedEmail, EmailConfirmed, 
                                     PasswordHash, SecurityStamp, ConcurrencyStamp, PhoneNumber, PhoneNumberConfirmed, 
                                     TwoFactorEnabled, LockoutEnabled, AccessFailedCount, FullName, IsActive, CreatedAt)
            VALUES (?, ?, ?, ?, ?, 1, 
                    'AQAAAAIAAYagAAAAEP+dummyHash', ?, ?, ?, 0, 
                    0, 1, 0, ?, 1, ?)
        ''', (u_id, email, email.upper(), email, email.upper(), str(uuid.uuid4()), str(uuid.uuid4()), phone, name, now))
        
        cur.execute("SELECT Id FROM AspNetRoles WHERE Name = 'Customer'")
        r_row = cur.fetchone()
        if r_row:
            cur.execute('INSERT OR IGNORE INTO AspNetUserRoles (UserId, RoleId) VALUES (?, ?)', (u_id, r_row[0]))
        print(f'Created user: {name} ({email})')

# Get user map: email -> Id
cur.execute('SELECT Email, Id FROM AspNetUsers')
user_map = {r[0]: r[1] for r in cur.fetchall()}

# 4. Rich Reviews Data for all 15 movies
# Format: (MovieId, UserEmail, Rating, Comment, Status (1=Published, 2=Hidden), DaysAgo)
reviews_data = [
    # 1. Avengers: Endgame
    (1, 'nguyenvana@gmail.com', 5, 'Trận đại chiến cuối cùng quá mãn nhãn và xúc động! Khoảnh khắc Avengers Assemble và sự hy sinh của Iron Man khiến cả rạp vỡ òa nước mắt. Phim hay nhất của vũ trụ Marvel!', 1, 14),
    (1, 'tranthib@gmail.com', 5, 'Đỉnh cao điện ảnh siêu anh hùng! Kỹ xảo CGI 10/10, âm thanh Dolby Atmos tại rạp nghe rung chuyển ghế. Rất xứng đáng với 3 tiếng ngồi rạp!', 1, 10),
    (1, 'levanc@gmail.com', 4, 'Phim rất xúc động, mạch phim phần đầu hơi chậm nhưng nửa sau bùng nổ nghẹt thở. Cảm ơn Marvel vì một tuổi thơ tuyệt vời.', 1, 5),
    (1, 'phamthid@gmail.com', 5, 'Xem lại lần thứ 2 tại rạp vẫn nổi da gà. Diễn xuất của Robert Downey Jr. và Chris Evans quá xuất sắc.', 1, 2),

    # 2. Spider-Man: Across the Spider-Verse
    (2, 'levanc@gmail.com', 5, 'Đồ họa và phong cách hoạt hình vượt trên mọi chuẩn mực! Mỗi vũ trụ một phong cách vẽ riêng biệt cực kỳ sáng tạo. Nhạc phim và cốt truyện cuốn hút từ đầu đến cuối.', 1, 18),
    (2, 'tranthib@gmail.com', 5, 'Một kiệt tác nghệ thuật thị giác! Diễn biến tâm lý của Miles Morales và Gwen Stacy chạm tới cảm xúc. Xem trên màn hình lớn thực sự choáng ngợp!', 1, 12),
    (2, 'vuthimai@gmail.com', 4, 'Phim siêu cuốn, màu sắc sống động bùng nổ thị giác. Điểm trừ duy nhất là kết thúc mở để chờ phần tiếp theo làm háo hức quá.', 1, 6),

    # 3. Oppenheimer
    (3, 'hoange@gmail.com', 5, 'Đúng chất bậc thầy Christopher Nolan! Âm thanh vụ nổ Trinity khiến cả rạp nín thở thót tim. Cillian Murphy diễn xuất bằng ánh mắt quá đỉnh cao, xứng đáng tượng vàng Oscar.', 1, 20),
    (3, 'doquanghuy@gmail.com', 5, 'Phim lịch sử khoa học kịch tính như phim hành động. Âm nhạc của Ludwig Göransson dồn dập tạo cảm giác căng thẳng tột độ.', 1, 15),
    (3, 'nguyenvana@gmail.com', 4, 'Hội thoại dày đặc đòi hỏi tập trung cao độ, nhưng từng chi tiết đều đắt giá. Một tác phẩm điện ảnh kinh điển thực thụ.', 1, 8),
    (3, 'buithutrang@gmail.com', 1, 'Phim nhiều lời thoại và thuật ngữ khoa học quá, hơi khó theo dõi với người xem phổ thông...', 2, 7), # Hidden

    # 4. Doraemon: Nobita và Bản Giao Hưởng Địa Cầu
    (4, 'tranthib@gmail.com', 5, 'Phim hoạt hình dễ thương, âm nhạc giao hưởng du dương tuyệt vời! Cả người lớn lẫn trẻ em đều thích mê. Rất thích hợp đi xem cùng gia đình cuối tuần.', 1, 16),
    (4, 'buithutrang@gmail.com', 4, 'Đưa bé nhà mình đi xem mà mẹ cũng khóc theo. Tình bạn của nhóm bạn Nobita và thông điệp âm nhạc kết nối trái đất rất ý nghĩa.', 1, 9),
    (4, 'levanc@gmail.com', 5, 'Hình ảnh vẽ cực đẹp, âm thanh rạp chiếu sống động. Mỗi mùa hè được xem một phần Doraemon là niềm vui trọn vẹn của tuổi thơ.', 1, 3),

    # 5. Mai
    (5, 'phamthid@gmail.com', 5, 'Phim xúc động sâu sắc, phản ánh chân thực số phận người phụ nữ và áp lực gia đình. Phương Anh Đào và Tuấn Trần diễn xuất quá ăn ý, khóc ướt cả khăn giấy.', 1, 22),
    (5, 'nguyenphuctien@gmail.com', 4, 'Góc quay và màu phim rất đẹp, chất lượng âm thanh tốt. Kịch bản lắng đọng, câu thoại thấm thía để lại nhiều suy ngẫm sau khi bước ra khỏi rạp.', 1, 13),
    (5, 'tranthib@gmail.com', 4, 'Trấn Thành đã làm một bộ phim rất chỉn chu và cảm xúc. Rạp CineStar phục vụ bắp nước ngon, ghế ngồi êm ái.', 1, 4),

    # 6. Quật Mộ Trùng Ma (Exhuma)
    (6, 'doquanghuy@gmail.com', 5, 'Phim kinh dị tâm linh Hàn Quốc quá xuất sắc! Yếu tố phong thủy, trừ tà và lịch sử đan xen nghẹt thở. Kim Go Eun và Lee Do Hyun diễn đỉnh chóp!', 1, 25),
    (6, 'vuthimai@gmail.com', 5, 'Không khí u ám, rùng rợn bao trùm từ đầu đến cuối. Âm thanh rạp hiệu ứng vòm chân thực làm giật thót tim mấy phen. Đáng tiền vé!', 1, 17),
    (6, 'nguyenvana@gmail.com', 4, 'Nửa đầu phim không khí cực kỳ cuốn hút và ma mị, nửa sau hơi hướng hành động nhưng vẫn rất hồi hộp và thỏa mãn.', 1, 11),

    # 7. Fast & Furious X
    (7, 'nguyenphuctien@gmail.com', 4, 'Phim hành động thuần giải trí đỉnh cao! Những pha đua xe cháy nổ bất chấp vật lý xem cực kỳ đã mắt. Jason Momoa đóng phản diện quái chiêu rất cuốn hút.', 1, 19),
    (7, 'levanc@gmail.com', 4, 'Xem rạp âm thanh gầm rú của động cơ xe phê chữ ê kéo dài. Đi cùng hội bạn xem giải trí cuối tuần xả stress cực chuẩn.', 1, 14),
    (7, 'hoange@gmail.com', 3, 'Kịch bản hơi phi lý nhưng xem kỹ xảo hành động thì vẫn rất sướng và mãn nhãn.', 1, 6),

    # 8. Cô Dâu Hào Môn
    (8, 'buithutrang@gmail.com', 4, 'Kịch bản trào phúng thú vị về gia đình giả giàu để đổi đời. Diễn xuất của Uyển Ân và Thu Trang rất duyên dáng, mang lại nhiều tiếng cười sảng khoái.', 1, 12),
    (8, 'phamthid@gmail.com', 4, 'Phục trang và bối cảnh xa hoa lộng lẫy. Phim nhẹ nhàng, hài hước, xem vừa giải trí vừa thấy được giá trị của tình cảm gia đình.', 1, 5),

    # 9. Dune: Part Two
    (9, 'hoange@gmail.com', 5, 'Tuyệt phẩm khoa học viễn tưởng vĩ đại của thập kỷ! Sa mạc Arrakis hiện lên kỳ vĩ, đàn sâu cát khổng lồ choáng ngợp. Bắt buộc phải xem trên màn hình lớn!', 1, 24),
    (9, 'nguyenvana@gmail.com', 5, 'Âm thanh của Hans Zimmer gầm vang rung chuyển cả lồng ngực. Diễn xuất của Timothée Chalamet và Zendaya thăng hoa tột bậc.', 1, 16),
    (9, 'doquanghuy@gmail.com', 5, 'Xứng đáng từng xu tiền vé! Mãn nhãn về cả phần nhìn lẫn phần nghe, nhịp phim kịch tính không rời mắt được một giây.', 1, 8),

    # 10. Kung Fu Panda 4
    (10, 'tranthib@gmail.com', 5, 'Gấu Po trở lại vẫn đáng yêu và tấu hài như ngày nào! Các màn võ thuật kết hợp hoạt hình mượt mà, rạp chiếu đông vui cười rôm rả.', 1, 15),
    (10, 'buithutrang@gmail.com', 4, 'Phim ngắn gọn, vui nhộn, hình ảnh rực rỡ sắc màu. Các bạn nhỏ đi xem thích mê, combo bắp nước ngọt ngào rất ngon.', 1, 7),

    # 11. Deadpool & Wolverine
    (11, 'nguyenvana@gmail.com', 5, 'Cặp đôi hoàn hảo Ryan Reynolds và Hugh Jackman! Hài bựa cực đỉnh, các màn cameo bất ngờ khiến cả rạp hò reo phấn khích. Phim Marvel đỉnh nhất năm!', 1, 18),
    (11, 'levanc@gmail.com', 5, 'Đánh đấm bạo lực máu lửa đúng chuẩn 18+, nhạc phim thập niên 90-2000 chọn quá chất. Cười nghiêng ngả từ phút đầu đến tận cảnh after-credit.', 1, 10),
    (11, 'nguyenphuctien@gmail.com', 5, 'Xem giải trí đã đời luôn! Fan cứng Marvel không thể bỏ qua bộ phim này.', 1, 4),
    (11, 'hoange@gmail.com', 5, '[SPOILER NỘI DUNG] Xuất hiện cả Blade và Gambit chiến đấu cùng nhau cực kỳ mãn nhãn!', 2, 3), # Hidden

    # 12. Inside Out 2
    (12, 'phamthid@gmail.com', 5, 'Pixar không bao giờ làm khán giả thất vọng! Nhân vật Lo Âu (Anxiety) được xây dựng quá chân thực, xem mà thấy đồng cảm sâu sắc. Rơi nước mắt vì thấy lại chính mình.', 1, 21),
    (12, 'vuthimai@gmail.com', 5, 'Một bài học tâm lý trưởng thành vô cùng nhân văn cho cả người lớn. Phim sâu sắc, ấm áp và đong đầy tình yêu thương.', 1, 14),
    (12, 'buithutrang@gmail.com', 4, 'Màu sắc tươi sáng, các nhân vật cảm xúc mới cực kỳ đáng yêu. Rất khuyên mọi người nên đi xem để ôm lấy những cảm xúc bên trong mình.', 1, 5),

    # 13. Lật Mặt 7: Một Điều Ước
    (13, 'nguyenvana@gmail.com', 5, 'Phim của anh Lý Hải lần này chạm đến tận cùng cảm xúc tình mẫu tử. Câu chuyện bà Hai và những người con khiến cả rạp nghẹn ngào, khóc nức nở.', 1, 26),
    (13, 'tranthib@gmail.com', 5, 'Diễn xuất của má Thanh Hiền quá chân thật, mộc mạc và lay động lòng người. Phim gia đình Việt Nam hay nhất năm nay!', 1, 19),
    (13, 'doquanghuy@gmail.com', 5, 'Xem xong chỉ muốn gọi điện ngay về cho mẹ. Thông điệp hiếu thảo thiêng liêng và ý nghĩa vô cùng.', 1, 9),

    # 14. Godzilla x Kong: Đế Chế Mới
    (14, 'levanc@gmail.com', 5, 'Quái thú choảng nhau từ lòng đất lên mặt đất rung chuyển cả rạp! Kỹ xảo CGI quá khủng, Kong đeo găng tay điện tử đấm cực kỳ uy lực.', 1, 17),
    (14, 'hoange@gmail.com', 4, 'Hành động liên tục không ngơi nghỉ, kỹ xảo hoành tráng xem cực kỳ giải trí và đã mắt. Âm thanh rạp đập rung sàn.', 1, 8),

    # 15. Twisters
    (15, 'doquanghuy@gmail.com', 4, 'Kỹ xảo tái hiện bão xoáy kinh hoàng chân thực đến rợn người! Âm thanh rít gầm của gió lốc làm thót tim. Trải nghiệm xem rạp cực kỳ hồi hộp.', 1, 13),
    (15, 'nguyenphuctien@gmail.com', 4, 'Phim kịch tính nghẹt thở, diễn viên trẻ đẹp diễn xuất tự nhiên. Một bộ phim thảm họa thiên nhiên rất đáng xem ngoài rạp.', 1, 6)
]

# Clear old reviews and re-insert rich demo reviews
cur.execute('DELETE FROM Reviews')
print('Cleared old reviews.')

now = datetime.datetime.now()
inserted = 0
for movie_id, email, rating, comment, status, days_ago in reviews_data:
    u_id = user_map.get(email)
    if not u_id:
        print(f'Warning: User {email} not found!')
        continue
    created_at = (now - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('''
        INSERT INTO Reviews (MovieId, UserId, Rating, Comment, Status, CreatedAt)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (movie_id, u_id, rating, comment, status, created_at))
    inserted += 1

print(f'Successfully inserted {inserted} reviews for all 15 movies!')

# 5. Recalculate Movie.Rating based on Published reviews
for m_id in range(1, 16):
    cur.execute('SELECT AVG(Rating) FROM Reviews WHERE MovieId = ? AND Status = 1', (m_id,))
    avg = cur.fetchone()[0]
    if avg is not None:
        rating_val = round(avg, 1)
    else:
        rating_val = 5.0
    cur.execute('UPDATE Movies SET Rating = ? WHERE MovieId = ?', (rating_val, m_id))

print('Recalculated Movie Ratings based on published reviews!')

conn.commit()
conn.close()
print('publish/app.db updated successfully!')
