#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <pageshowresult.h>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_btnCS_clicked();

    void on_csReturn_clicked();

    void on_btnRI_clicked();

    void on_riReturn_clicked();

    void on_btnMI_clicked();

    void on_miReturn_clicked();

    void on_btnSR_clicked();

private:
    Ui::MainWindow *ui;
    pageShowResult *pSR = new pageShowResult;
};

#endif // MAINWINDOW_H
