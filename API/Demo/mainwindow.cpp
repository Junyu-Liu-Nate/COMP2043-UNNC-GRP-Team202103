#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    int x = this->frameGeometry().width();
    int y = this->frameGeometry().height();
    ui->stackedWidget->setGeometry(0, 0, x, y);

    this->setWindowTitle("OVERLAP");
    this->setWindowIcon(QIcon(":/images/images/icon.png"));
}

MainWindow::~MainWindow()
{
    delete ui;
}

//主界面的choose style, random input,
//manual input按钮作用，在.h里有声明
void MainWindow::on_btnCS_clicked()
{
    //抓取路径https://blog.csdn.net/liyuanbhu/article/details/53710249
    //合并的时候把绝对路径抓出来放进样式表里
    ui->csBtnCub->setStyleSheet("image: url(D:/QtRes/cubes.png);");
    ui->csBtnCircle->setStyleSheet("image: url(D:/QtRes/circles.png);");
    ui->stackedWidget->setCurrentIndex(1);
}

void MainWindow::on_csReturn_clicked()
{
    ui->stackedWidget->setCurrentIndex(0);
}

//点击Random Input后，读取txt文件并允许用户更改
//读取+展示+写入（更新）
#include <QDebug>
#include <QString>
void MainWindow::on_btnRI_clicked()
{
    QString path = "D:/QtRes/input.txt";
    //qDebug()<<"path: "<<path;
    QFile fp(path);
    if(!fp.open(QIODevice::ReadOnly|QIODevice::Text))
    {
        qDebug()<<"FileOpenError"<<fp.errorString();
    }
    QByteArray content = fp.readAll();
    //qDebug()<<content;//展示内容
    ui->textRI->setPlainText(content);
    fp.close();

    ui->stackedWidget->setCurrentIndex(2);

    //测试路径
    /*
    QString path;
    path = QCoreApplication::applicationDirPath();
    qDebug() << "path: " << path;
    */

    //QFile fp("C:/Users/Lenovo/Desktop/QT/build-Demo3-Desktop_Qt_5_9_0_MinGW_32bit-Debug/debug/runFile.txt");
    /*
    QFile fp(":/new/text/text/runFile.txt");
    //这里不可以随便改成ReadWrite
    if(!fp.open(QIODevice::ReadOnly|QIODevice::Text))
    {
        //qDebug()<<"FileOpenError"<<fp.errorString();
        //fp.close();
        qDebug()<<"FileOpenError"<<fp.errorString();
    }
    QByteArray content = fp.readAll();
    qDebug()<<content;
    ui->textRI->setPlainText(content);
    fp.close();
    */
}

void MainWindow::on_riReturn_clicked()
{
    QString str = ui->textRI->toPlainText();
    QByteArray content = str.toUtf8();
    QString path = "D:/QtRes/input.txt";
    QFile fp(path);
    if(!fp.open(QIODevice::WriteOnly|QIODevice::Text|QIODevice::Truncate))//Truncate清空
    {
        qDebug()<<"FileWriteError"<<fp.errorString();
    }
    fp.write(content, content.length());
    fp.close();

    /*
    QString str = ui->textRI->toPlainText();
    QByteArray content = str.toUtf8();

    QFile fp(":/new/text/text/runFile.txt");
    qDebug()<<content;
    if(!fp.open(QIODevice::WriteOnly|QIODevice::Text))
    {
        qDebug()<<"FileOpenError"<<fp.errorString();//FileOpenError "Unknown error"
    }
    fp.write(content, content.length());//QIODevice::write (QFile, ":\new\text\text\runFile.txt"): device not open
    //fp.write(content);
    fp.close();
    */

    ui->stackedWidget->setCurrentIndex(0);
}

void MainWindow::on_btnMI_clicked()
{
    ui->stackedWidget->setCurrentIndex(3);
}

//Manual Input的内容保存
void MainWindow::on_miReturn_clicked()
{
    QString str = ui->textMI->toPlainText();
    QByteArray content = str.toUtf8();
    QString path = "D:/QtRes/input.txt";
    QFile fp(path);
    if(!fp.open(QIODevice::WriteOnly|QIODevice::Text|QIODevice::Truncate))//Truncate清空
    {
        qDebug()<<"FileWriteError"<<fp.errorString();
    }
    fp.write(content, content.length());
    fp.close();

    ui->stackedWidget->setCurrentIndex(0);
}

//显现最后一格页面
#include <pageshowresult.h>
void MainWindow::on_btnSR_clicked()
{
    this->hide();
    //pageShowResult *pSR = new pageShowResult;
    pSR->show();
    //pSR->centralWidget()->setStyleSheet("image: url(D:/QtRes/cubes.png);");//背景
}
