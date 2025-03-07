import streamlit as st
 
html_content=""
def info_plates():

    html_content = """

    <title>Info Plate Container</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* Container for Info Plates */
        .info-plate-container {
            width: fit-content;
            max-width: 100%;
            height: 50vh; /* 40% of the screen height */
            overflow-y: auto; /* Vertical scrolling */
            overflow-x: hidden; /* Hide horizontal overflow */
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            displayflex;
            justify-content:center;
        }

        /* Info Plate Styling */
        .info-plate {
            width: 600px;
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 20px;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background: linear-gradient(135deg, #f9f9f9, #ffffff);
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 15px; /* Space between Info Plates */
        }

        .info-plate:last-child {
            margin-bottom: 0; /* Remove margin for the last Info Plate */
        }

        /* Hover Effect for Info Plate */
        .info-plate:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }

        /* Movie Name Styling */
        .movie-name {
            display: block;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
            position: relative;
        }

        /* Underline Animation for Movie Name */
        .movie-name::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: -5px;
            width: 50px;
            height: 3px;
            background-color: #f5b301; /* Golden Color */
            transition: width 0.3s ease;
        }

        .info-plate:hover .movie-name::after {
            width: 100%;
        }

        /* Details Row Styling */
        .details-row {
            display: flex;
            gap: 15px;
            margin-bottom: 12px;
        }

        .detail-item {
            font-size: 14px;
            color: #666;
            position: relative;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Star Icon Styling */
        .score-icon {
            color: #f5b301; /* Golden Color */
            font-size: 14px;
        }

        /* Tooltip Styling */
        .detail-item[data-tooltip]:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            background: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            left: 50%;
            top: 10%;
            transform: translate(-50%, -100%);
            margin-left: 0;
            z-index: 1;
            opacity: 0;
            transition: opacity 0.2s;
        }

        .detail-item[data-tooltip]:hover::after {
            opacity: 1;
        }

        /* Genre and Voting Row Styling */
        .genre-voting-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .genre {
            font-size: 14px;
            color: #444;
            font-style: italic;
           
        }

        /* Voting Count Styling with Icon */
        .votes-count {
            background-color: #eee;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .votes-count i {
            color: #666;
        }

        /* Background Decoration */
        .info-plate::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(245, 179, 1, 0.1) 10%, transparent 10.01%);
            background-size: 20px 20px;
            transform: rotate(45deg);
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        .info-plate:hover::before {
            opacity: 1;
        }
            </style>
            </head>"""
    return html_content


def info_body():
    body="""<body>
    <div class="info-plate-container">
        <!-- Info Plate 1 -->
        <div class="info-plate">
            <div class="movie-name">The Movie Title 1</div>
            <div class="details-row">
                <span class="detail-item" data-tooltip="Movie Rating">
                    <i class="fas fa-film"></i>
                    Rating: PG-13
                </span>
                <span class="detail-item" data-tooltip="Duration">
                    <i class="fas fa-clock"></i>
                    2h 18min
                </span>
                <span class="detail-item" data-tooltip="MYMDb Score">
                    <i class="fas fa-star score-icon"></i>
                    Score: 8.5/10
                </span>
            </div>
            <div class="genre-voting-row">
                <div class="genre" data-tooltip="Movie Genre">
                    <i class="fas fa-tags"></i>
                    Action, Adventure
                </div>
                <div class="votes-count" >
                    <i class="fas fa-thumbs-up"></i>
                    Votes: 1.2K
                </div>
            </div>
        </div> """
    return body
