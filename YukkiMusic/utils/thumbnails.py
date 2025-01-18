#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License .
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

# Ukuran gambar
width, height = 1080, 720

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]


def crop_center_rounded_rectangle(img, output_size, border, corner_radius, crop_scale=1.5):
    half_width = img.size[0] / 2
    half_height = img.size[1] / 2
    larger_size = int(output_size * crop_scale)

    img = img.crop(
        (
            half_width - larger_size / 2,
            half_height - larger_size / 2,
            half_width + larger_size / 2,
            half_height + larger_size / 2,
        )
    )
    img = img.resize((output_size - 2 * border, output_size - 2 * border))

    final_img = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
    mask_main = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    draw_main = ImageDraw.Draw(mask_main)
    draw_main.rounded_rectangle(
        (0, 0, output_size - 2 * border, output_size - 2 * border), radius=corner_radius, fill=255
    )
    final_img.paste(img, (border, border), mask_main)
    return final_img


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_v4.png"):
        return f"cache/{videoid}_v4.png"
    
    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)

    try:
        for result in (await results.next())["result"]:
            title = result.get("title", "Unsupported Title")
            title = re.sub("\W+", " ", title).title()

            duration = result.get("duration", "Unknown Mins")
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")

            if "thumbnails" in result and len(result["thumbnails"]) > 0:
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            else:
                raise ValueError("Thumbnail not found in search results")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                            await f.write(await resp.read())
            
            youtube = Image.open(f"cache/thumb{videoid}.png")
            image1 = changeImageSize(1280, 720, youtube)
            image2 = image1.convert("L")
            background = image2.filter(ImageFilter.BoxBlur(20)).convert("RGBA")
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)

            draw = ImageDraw.Draw(background)
            font = ImageFont.truetype("SprotifyMusic/assets/Montserrat-Medium.ttf", 20)
            title_font = ImageFont.truetype("SprotifyMusic/assets/Montserrat-Bold.ttf", 45)

            # Rounded rectangle thumbnail
            corner_radius = 50
            rectangle_thumbnail = crop_center_rounded_rectangle(youtube, 400, 20, corner_radius)
            rectangle_position = (120, 160)
            background.paste(rectangle_thumbnail, rectangle_position, rectangle_thumbnail)


            # Menghitung ukuran teks menggunakan textbbox
            title1 = truncate(title)
            text_bbox_1 = draw.textbbox((0, 0), title1[0], font=title_font)
            text_bbox_2 = draw.textbbox((0, 0), title1[1], font=title_font)

            # Mendapatkan ukuran rectangle
            text_width = max(text_bbox_1[2] - text_bbox_1[0], text_bbox_2[2] - text_bbox_2[0])  # Lebar rectangle = lebar teks terpanjang
            text_height = (text_bbox_1[3] - text_bbox_1[1]) + (text_bbox_2[3] - text_bbox_2[1]) + 20  # Tinggi rectangle = tinggi kedua baris teks + padding
            padding = 20  # Jarak tambahan di sekitar teks
            rectangle_width = text_width + 2 * padding
            rectangle_height = text_height + 2 * padding

            # Koordinat untuk rectangle
            rectangle_x = 565  # Posisi X rectangle
            rectangle_y = 180  # Posisi Y rectangle (dimulai dari baris pertama teks)
            rectangle_coords = (
                rectangle_x, 
                rectangle_y, 
                rectangle_x + rectangle_width, 
                rectangle_y + rectangle_height
            )

            # Gambar rounded rectangle hanya dengan outline
            rounded_rectangle_radius = 20  # Radius sudut rounded rectangle
            outline_color = "white"  # Warna outline
            draw.rounded_rectangle(
                rectangle_coords, 
                radius=rounded_rectangle_radius, 
                outline=outline_color, 
                width=3  # Ketebalan outline
            )

            # Menempatkan teks di tengah rectangle
            text_x = rectangle_x + padding
            text_y_1 = rectangle_y + padding  # Posisi baris pertama teks
            text_y_2 = text_y_1 + (text_bbox_1[3] - text_bbox_1[1]) + 10  # Posisi baris kedua teks (dengan jarak 10px)

            # Text
            title1 = truncate(title)
            draw.text((text_x, text_y_1), title1[0], fill="white", font=title_font)
            draw.text((text_x, text_y_2), title1[1], fill="white", font=title_font)
            draw.text((565, 350), f"{channel} | {views}", fill="white", font=font)
            draw.text((10, 10), "Sprotify Music", fill="white", font=title_font)

            try:
                os.remove(f"cache/thumb{videoid}.png")
            except:
                pass

            background.save(f"cache/{videoid}_v4.png")
            return f"cache/{videoid}_v4.png"

    except Exception as e:
        print(f"Thumbnails Error: {e}")
        raise


"""
    try:
        query = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception as e:
        return f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"


async def gen_qthumb(vidid):
    try:
        query = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception as e:
        return f"https://img.youtube.com/vi/{vidid}/maxresdefault.jpg"
"""