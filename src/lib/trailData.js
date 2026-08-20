import { writable } from "svelte/store";

export const trails = writable([
    {
        "idKey": 301,
        "name": "‘Ōhi‘a Trail",
        "island": "HAWAII",
        "difficulty": null,
        "lengthMiles": 1.80,
        "lengthKm": 2.90,
        "elevationFeet": 472.00,
        "elevationMeters": 143.87,
        "activities": [
            "TOURS",
            "BICYCLE",
            "DOG_ON_LEASH",
            "EQUINE",
            "WILDLIFE_VIEW",
            "PEDESTRIAN",
            "SIGHTSEEING",
            "HIKING"
        ],
        "coords": {
            "idKey": 625,
            "latitude": 19.79687340012338,
            "longitude": -155.83717179318074
        },
        "closed": true,
        "vendorClosed": false,
        "kmlFiles": [
            {
                "idKey": 4198,
                "fileName": "2tyvhgkznullA5hANhsZM.kmz",
                "uploadType": "KML",
                "originalName": "Ohia Trail.kmz",
                "extension": "kmz",
                "size": 5711,
                "checksum": "8ad29aaf",
                "hash": "2tyvhgkznullA5hANhsZM",
                "mimeType": "application/vnd.google-earth.kmz",
                "verified": true,
                "filePath": "/2t/yv/",
                "title": "Ohia Trail",
                "comments": null,
                "altText": null,
                "file": null,
                "thumbSm": null,
                "thumbMd": null,
                "thumbLg": null,
                "position": 99,
                "lalaUser": null,
                "dateDeleted": null,
                "dateCreated": 1602898556534,
                "dateModified": 1786788014307,
                "deleted": false,
                "thumbSmName": null,
                "thumbMdName": null,
                "thumbLgName": null,
                "image": false
            }
        ],
        "inactive": false
    }
])