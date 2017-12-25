# EpicMonopoly
[![Build Status](https://travis-ci.com/Spacebody/EpicMonopoly-Server.svg?token=MNpGaGjQxonn6yLX6TwY&branch=master)](https://travis-ci.com/Spacebody/EpicMonopoly-Server)

A novel developed monopoly based on web: EpicMonopoly 

Game Logic development:

- [x] Game logic
- [x] Json design
- [x] Demo
- [ ] Communications(Developing) 

## TODO
- [ ] Trade 
- [ ] EF
- [ ] board: new_board(Shelved)

## Bug
- [ ] some function in bank(add loan dict, remove loan dict, repayment)

Server structure: 

- [ ] Web server: nginx
- [ ] Database: mongoDB
- [ ] Application server: tornado
- [ ] Cache server: redis(Shelved)

## Details

- Web server is used to listen in the port and deal with queries from front end directly, for:
	+ static page query will be handled in nginx
	+ dynamic page query will be transfer to application server
- Application is used to deal with game logic and the query sent from nginx
- Database stores game data and is used for data IO operation. Main database is mongoDB
- Redis is not the main database but is used as a cache server for accelerating

## Reference
- Google
- Monopoly 5(game)
- MongoDB
	- PyMongo 
- Nginx
- Tornado offical guide
	- [Introduction to Tornado](https://mirrors.segmentfault.com/itt2zh/)
	- [中文官方文档](http://www.tornadoweb.cn/documentation)
	- [英文官方文档](http://www.tornadoweb.org/en/stable/index.html)
- Wiki