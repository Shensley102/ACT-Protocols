// SwiftUI search over act_protocol_index.json (place JSON in app bundle)
import SwiftUI

struct ProtocolItem: Codable, Identifiable {
    let id = UUID()
    let title: String
    let number: String
    let category: String
    let start_page: Int
    let end_page: Int
    let excerpt: String
}

struct IndexData: Codable {
    let source_pdf: String
    let num_pages: Int
    let protocols: [ProtocolItem]
}

func tokenize(_ s: String) -> [String] {
    let stop: Set<String> = ["a","an","and","are","as","at","be","but","by","for","from","has","have","if","in","into","is","it","its","of","on","or","that","the","their","them","there","they","this","to","was","were","will","with","your"]
    let ns = s.lowercased() as NSString
    let regex = try! NSRegularExpression(pattern: "[A-Za-z0-9']{2,}")
    return regex.matches(in: s, range: NSRange(location: 0, length: ns.length)).map { ns.substring(with: $0.range) }.filter { !stop.contains($0) }
}

func score(_ query: [String], item: ProtocolItem) -> Int {
    let title = tokenize(item.title)
    let excerpt = tokenize(item.excerpt)
    var s = 0
    for t in query {
        s += excerpt.filter { $0 == t }.count
        s += 3 * title.filter { $0 == t }.count
    }
    return s
}

struct ContentView: View {
    @State private var query = ""
    @State private var data = IndexData(source_pdf: "", num_pages: 0, protocols: [])
    @State private var filtered: [ProtocolItem] = []

    var body: some View {
        NavigationView {
            VStack {
                TextField("Search...", text: $query)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding(.horizontal)

                List(filtered) { item in
                    VStack(alignment: .leading, spacing: 4) {
                        Text(item.title).font(.headline)
                        Text("\(item.category) • pages \(item.start_page)-\(item.end_page)").font(.caption).foregroundColor(.secondary)
                        Text(item.excerpt).font(.caption)
                    }
                }
            }
            .navigationTitle("Protocols")
        }
        .onAppear {
            if let url = Bundle.main.url(forResource: "act_protocol_index", withExtension: "json"),
               let dataRaw = try? Data(contentsOf: url),
               let parsed = try? JSONDecoder().decode(IndexData.self, from: dataRaw) {
                data = parsed
                filtered = parsed.protocols
            }
        }
        .onChange(of: query) { newValue in
            let terms = tokenize(newValue)
            if terms.isEmpty {
                filtered = data.protocols
            } else {
                filtered = data.protocols
                    .map { (score(terms, item: $0), $0) }
                    .filter { $0.0 > 0 }
                    .sorted { $0.0 > $1.0 }
                    .map { $0.1 }
            }
        }
    }
}
