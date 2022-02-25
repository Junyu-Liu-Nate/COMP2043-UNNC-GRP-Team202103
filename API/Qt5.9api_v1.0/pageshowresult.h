#ifndef PAGESHOWRESULT_H
#define PAGESHOWRESULT_H

#include <QMainWindow>

namespace Ui {
class pageShowResult;
}

class pageShowResult : public QMainWindow
{
    Q_OBJECT

public:
    explicit pageShowResult(QWidget *parent = 0);
    ~pageShowResult();
    //void paintEvent(QPaintEvent *event);//放置图片

private slots:
    void on_actShowDIFF_triggered();

    void on_actChangeStyle_triggered();

    void on_actFeedback_triggered();

    void on_actDownload_triggered();

private:
    Ui::pageShowResult *ui;
};

#endif // PAGESHOWRESULT_H
