from app.database import models

class TestModelTest():
    def test_command(self, db_session):
        command = models.Command(b"h", bytearray.fromhex("03"), b"Q")
        db_session.add(command)
        db_session.commit()

        resp = db_session.query(models.Command).get(1)
        assert resp.read == b"h"
        assert resp.write == bytearray.fromhex("03")
        assert resp.calibrate == b"Q"

    def test_create_full(self, db_session):
        command = models.Command(b"r", bytearray.fromhex("03"), b"C")
        

