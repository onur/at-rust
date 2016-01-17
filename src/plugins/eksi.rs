

use at::{AtRust, AtTrigger};
use plugins::get;

use select::document::Document;
use select::predicate::{Attr, Class, Name};
use rand;



pub fn get_eksi(query: &str) -> Option<Vec<String>> {

    let url = format!("https://eksisozluk.com/{}", query);

    let body = match get(&url[..]) {
        Some(n) => n,
        None => return None,
    };

    let document = Document::from_str(&body[..]);

    let mut entries: Vec<String> = Vec::new();

    for entry in document.find(Attr("id", "entry-list")).find(Name("li")).iter() {
        let entry_text = entry.find(Class("content")).first().unwrap().text();
        // FIXME: Do I really need to clone text?
        entries.push(entry_text.clone());
    }

    return match entries.len() {
        0 => None,
        _ => Some(entries),
    };

}


pub fn eksi(trigger: &AtTrigger, at: &AtRust) {

    let entries = get_eksi(&trigger.command_message[..]);

    match entries {
        Some(entries) => {
            at.reply(trigger,
                     &entries[rand::random::<usize>() % entries.len()][..])
        }
        None => {}
    }

}
