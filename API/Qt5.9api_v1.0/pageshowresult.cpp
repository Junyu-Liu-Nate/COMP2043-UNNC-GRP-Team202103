#include "pageshowresult.h"
#include "ui_pageshowresult.h"

pageShowResult::pageShowResult(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::pageShowResult)
{
    ui->setupUi(this);
    /*ui->stackedWidget->setVisible(false);//一开始不显示*/
    //在这里对第一个做事
    ui->overlappedIma->setStyleSheet("image: url(D:/QtRes/cubes.png);");

    this->setWindowTitle("OVERLAP");
    this->setWindowIcon(QIcon(":/images/images/icon.png"));

    //ui->toolBar->act
}

pageShowResult::~pageShowResult()
{
    delete ui;
}

//实现paintEvent
/*#include <QPainter>
void pageShowResult::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    QPainter painter(this);
    painter.drawPixmap(0, ui->toolBar->height(),
                       width(), height()-ui->toolBar->height(),
                       QPixmap(":/new/images/cubes.png"));
}*/

void pageShowResult::on_actShowDIFF_triggered()
{
    ui->stackedWidget->setCurrentIndex(1);

    ui->before->setStyleSheet("image: url(D:/QtRes/cubes.png);");
    ui->after->setStyleSheet("image: url(D:/QtRes/circles.png);");
}

//这里有个问题，没有设置再次展示overlapped image的按钮
//同时，这里的两个radio button的checked状态需要和前面的保持一致，怎么传输过来
void pageShowResult::on_actChangeStyle_triggered()
{
    ui->stackedWidget->setCurrentIndex(2);

    ui->altCub->setStyleSheet("image: url(D:/QtRes/cubes.png);");
    ui->altCirc->setStyleSheet("image: url(D:/QtRes/circles.png);");
}

//传到哪里...
void pageShowResult::on_actFeedback_triggered()
{
    ui->stackedWidget->setCurrentIndex(3);
}

//下载overlapped图片
#include <QFileDialog>
#include <QDebug>
void pageShowResult::on_actDownload_triggered()
{
    QString path = QFileDialog::getSaveFileName(this,
                                                       tr("Save Image"),
                                                       tr("overlapped.png"),
                                                       tr("(*.png)"));//返回路径
    //QImage image(":/new/text/images/cubes.png");
    QImage image("D:/QtRes/cubes.png");
    bool ret = image.save(path);
    if(!ret)
    {
        qDebug()<<"Save Fail!";
    }
}
