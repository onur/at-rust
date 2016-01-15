
pub mod eksi;

use std::io::Read;
use hyper::Client;
use hyper::header::Connection;


pub fn get(url: &str) -> Option<String> {

    let client = Client::new();

    let res = client.get(url)
        .header(Connection::close())
        .send();

    // FIXME: I don't think this is idomatic
    if res.is_err() {
        return None
    }

    let mut body = String::new();
    match res.unwrap().read_to_string(&mut body) {
        Ok(_) => return Some(body),
        Err(_) => return None
    }
}



#[test]
fn test_get() {
    let p = get("https://onur.im/");
    assert_eq!(true, p.is_some());
}

#[test]
fn test_get_fail_url() {
    let p = get("onur");
    assert_eq!(true, p.is_none());
}
